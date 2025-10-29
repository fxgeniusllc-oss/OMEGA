"""Blockchain interface for interacting with multiple chains."""
from typing import Dict, Optional
from web3 import Web3
from eth_account import Account
import asyncio


class BlockchainInterface:
    """Handles blockchain interactions across multiple chains."""
    
    def __init__(self, config):
        """Initialize blockchain interface."""
        self.config = config
        self.chains: Dict[str, Web3] = {}
        self._setup_chains()
    
    def _setup_chains(self):
        """Setup Web3 connections for all chains."""
        chain_configs = {
            "POLYGON": self.config.INFURA_POLYGON_RPC,
            "ETHEREUM": self.config.INFURA_ETHEREUM_RPC,
            "ARBITRUM": self.config.INFURA_ARBITRUM_RPC,
            "OPTIMISM": self.config.INFURA_OPTIMISM_RPC,
        }
        
        for chain_name, rpc_url in chain_configs.items():
            if rpc_url:
                try:
                    w3 = Web3(Web3.HTTPProvider(rpc_url))
                    if w3.is_connected():
                        self.chains[chain_name] = w3
                except Exception as e:
                    print(f"Failed to connect to {chain_name}: {e}")
    
    def get_chain(self, chain_name: str) -> Optional[Web3]:
        """Get Web3 instance for a specific chain."""
        return self.chains.get(chain_name.upper())
    
    async def get_balance(self, chain_name: str, address: str) -> float:
        """Get balance for an address on a specific chain."""
        w3 = self.get_chain(chain_name)
        if not w3:
            return 0.0
        
        try:
            balance_wei = w3.eth.get_balance(address)
            balance_eth = w3.from_wei(balance_wei, 'ether')
            return float(balance_eth)
        except Exception as e:
            print(f"Error getting balance: {e}")
            return 0.0
    
    async def get_gas_price(self, chain_name: str) -> int:
        """Get current gas price for a chain."""
        w3 = self.get_chain(chain_name)
        if not w3:
            return 0
        
        try:
            gas_price = w3.eth.gas_price
            return int(gas_price * self.config.GAS_PRICE_MULTIPLIER)
        except Exception as e:
            print(f"Error getting gas price: {e}")
            return 0
    
    async def estimate_gas(self, chain_name: str, transaction: dict) -> int:
        """Estimate gas for a transaction."""
        w3 = self.get_chain(chain_name)
        if not w3:
            return 0
        
        try:
            gas_estimate = w3.eth.estimate_gas(transaction)
            return gas_estimate
        except Exception as e:
            print(f"Error estimating gas: {e}")
            return 0
    
    async def send_transaction(self, chain_name: str, transaction: dict) -> Optional[str]:
        """Send a transaction on a specific chain."""
        w3 = self.get_chain(chain_name)
        if not w3 or self.config.MODE == "SIM":
            return None
        
        try:
            # Sign transaction
            if self.config.PRIVATE_KEY:
                account = Account.from_key(self.config.PRIVATE_KEY)
                signed_txn = w3.eth.account.sign_transaction(transaction, self.config.PRIVATE_KEY)
                tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                return w3.to_hex(tx_hash)
            return None
        except Exception as e:
            print(f"Error sending transaction: {e}")
            return None
    
    def is_connected(self, chain_name: str) -> bool:
        """Check if connected to a specific chain."""
        w3 = self.get_chain(chain_name)
        return w3 is not None and w3.is_connected()
