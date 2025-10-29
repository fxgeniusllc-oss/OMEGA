"""
Blockchain interface with multi-chain support and RPC fallback
"""
from typing import Dict, Optional, List
from web3 import Web3
try:
    from web3.middleware import geth_poa_middleware
except ImportError:
    # For newer versions of web3.py
    try:
        from web3.middleware.geth_poa import geth_poa_middleware
    except ImportError:
        # Fallback if middleware is not available
        geth_poa_middleware = None
from .config import config
from .utils.constants import CHAIN_IDS

class BlockchainInterface:
    """Multi-chain blockchain interface with automatic RPC fallback"""
    
    def __init__(self, logger=None):
        self.logger = logger
        self.w3_instances: Dict[str, Web3] = {}
        self.current_rpc_index: Dict[str, int] = {}
        self._initialize_connections()
    
    def _initialize_connections(self):
        """Initialize Web3 connections for all enabled chains"""
        for chain in config.enabled_chains:
            self.current_rpc_index[chain] = 0
            success = self._connect_to_chain(chain)
            if success:
                if self.logger:
                    self.logger.info(f"✓ Connected to {chain}")
            else:
                if self.logger:
                    self.logger.error(f"✗ Failed to connect to {chain}")
    
    def _connect_to_chain(self, chain: str, rpc_index: int = 0) -> bool:
        """Connect to a specific chain using RPC URL at given index"""
        rpc_urls = config.get_all_rpc_urls(chain)
        
        if not rpc_urls or rpc_index >= len(rpc_urls):
            return False
        
        rpc_url = rpc_urls[rpc_index]
        
        try:
            w3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={'timeout': 30}))
            
            # Add PoA middleware for chains that need it (Polygon, BSC, etc.)
            if chain in ['POLYGON', 'BSC'] and geth_poa_middleware:
                try:
                    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
                except Exception:
                    pass  # Middleware injection is optional
            
            # Test connection
            if w3.is_connected():
                self.w3_instances[chain] = w3
                self.current_rpc_index[chain] = rpc_index
                return True
            
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Failed to connect to {chain} RPC #{rpc_index + 1}: {str(e)}")
        
        # Try next RPC if available
        if rpc_index + 1 < len(rpc_urls):
            return self._connect_to_chain(chain, rpc_index + 1)
        
        return False
    
    def get_web3(self, chain: str) -> Optional[Web3]:
        """Get Web3 instance for a chain"""
        if chain not in self.w3_instances:
            # Try to connect
            self._connect_to_chain(chain)
        
        return self.w3_instances.get(chain)
    
    def reconnect_chain(self, chain: str) -> bool:
        """Reconnect to a chain using next available RPC"""
        current_index = self.current_rpc_index.get(chain, 0)
        rpc_urls = config.get_all_rpc_urls(chain)
        
        # Try next RPC
        next_index = (current_index + 1) % len(rpc_urls)
        
        if self.logger:
            self.logger.info(f"🔄 Switching {chain} to RPC #{next_index + 1}")
        
        return self._connect_to_chain(chain, next_index)
    
    def get_balance(self, chain: str, address: str) -> Optional[int]:
        """Get native token balance for an address"""
        w3 = self.get_web3(chain)
        if not w3:
            return None
        
        try:
            return w3.eth.get_balance(Web3.to_checksum_address(address))
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error getting balance for {address} on {chain}: {e}")
            # Try reconnecting
            if self.reconnect_chain(chain):
                return self.get_balance(chain, address)
            return None
    
    def get_token_balance(self, chain: str, token_address: str, wallet_address: str) -> Optional[int]:
        """Get ERC20 token balance"""
        w3 = self.get_web3(chain)
        if not w3:
            return None
        
        try:
            # Minimal ERC20 ABI for balanceOf
            erc20_abi = [
                {
                    "constant": True,
                    "inputs": [{"name": "_owner", "type": "address"}],
                    "name": "balanceOf",
                    "outputs": [{"name": "balance", "type": "uint256"}],
                    "type": "function"
                }
            ]
            
            token_contract = w3.eth.contract(
                address=Web3.to_checksum_address(token_address),
                abi=erc20_abi
            )
            
            balance = token_contract.functions.balanceOf(
                Web3.to_checksum_address(wallet_address)
            ).call()
            
            return balance
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error getting token balance on {chain}: {e}")
            return None
    
    def get_gas_price(self, chain: str) -> Optional[int]:
        """Get current gas price for a chain"""
        w3 = self.get_web3(chain)
        if not w3:
            return None
        
        try:
            gas_price = w3.eth.gas_price
            # Apply multiplier from config
            return int(gas_price * config.gas_price_multiplier)
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error getting gas price for {chain}: {e}")
            return None
    
    def get_block_number(self, chain: str) -> Optional[int]:
        """Get current block number"""
        w3 = self.get_web3(chain)
        if not w3:
            return None
        
        try:
            return w3.eth.block_number
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error getting block number for {chain}: {e}")
            # Try reconnecting
            if self.reconnect_chain(chain):
                return self.get_block_number(chain)
            return None
    
    def get_chain_id(self, chain: str) -> Optional[int]:
        """Get chain ID"""
        return CHAIN_IDS.get(chain)
    
    def is_connected(self, chain: str) -> bool:
        """Check if connected to a chain"""
        w3 = self.get_web3(chain)
        if not w3:
            return False
        
        try:
            return w3.is_connected()
        except Exception:
            return False
    
    def get_connection_status(self) -> Dict[str, bool]:
        """Get connection status for all chains"""
        status = {}
        for chain in config.enabled_chains:
            status[chain] = self.is_connected(chain)
        return status
    
    def estimate_gas(self, chain: str, transaction: dict) -> Optional[int]:
        """Estimate gas for a transaction"""
        w3 = self.get_web3(chain)
        if not w3:
            return None
        
        try:
            return w3.eth.estimate_gas(transaction)
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error estimating gas on {chain}: {e}")
            return None
