"""Flash loan manager for Balancer and Aave."""
from typing import Optional, Dict
from src.utils.constants import BALANCER_FLASH_LOAN_FEE, AAVE_FLASH_LOAN_FEE


class FlashLoanManager:
    """Handles flash loans from Balancer and Aave protocols."""
    
    def __init__(self, config, blockchain_interface, logger):
        """Initialize flash loan manager."""
        self.config = config
        self.blockchain = blockchain_interface
        self.logger = logger
        self.provider = config.FLASH_LOAN_PROVIDER
    
    def calculate_flash_loan_fee(self, amount: float) -> float:
        """
        Calculate flash loan fee based on provider.
        
        Args:
            amount: Loan amount in USD
        
        Returns:
            Fee amount in USD
        """
        if self.provider == "BALANCER":
            return amount * BALANCER_FLASH_LOAN_FEE
        elif self.provider == "AAVE":
            return amount * AAVE_FLASH_LOAN_FEE
        else:
            return amount * BALANCER_FLASH_LOAN_FEE
    
    def calculate_required_repayment(self, amount: float) -> float:
        """
        Calculate total repayment amount (principal + fee).
        
        Args:
            amount: Loan amount
        
        Returns:
            Total repayment amount
        """
        fee = self.calculate_flash_loan_fee(amount)
        return amount + fee
    
    async def request_flash_loan(
        self,
        token_address: str,
        amount: float,
        chain: str = "POLYGON"
    ) -> Optional[Dict]:
        """
        Request a flash loan.
        
        Args:
            token_address: Token contract address
            amount: Loan amount
            chain: Blockchain network
        
        Returns:
            Flash loan transaction details or None
        """
        fee = self.calculate_flash_loan_fee(amount)
        repayment = self.calculate_required_repayment(amount)
        
        self.logger.info(
            f"Requesting flash loan: {amount:.2f} on {chain} "
            f"via {self.provider} (Fee: {fee:.2f}, Repayment: {repayment:.2f})"
        )
        
        # In simulation mode, return mock data
        if self.config.MODE == "SIM":
            return {
                'provider': self.provider,
                'token': token_address,
                'amount': amount,
                'fee': fee,
                'repayment': repayment,
                'chain': chain,
                'status': 'SIMULATED'
            }
        
        # Real implementation would interact with Balancer/Aave contracts
        try:
            if self.provider == "BALANCER":
                return await self._request_balancer_flash_loan(
                    token_address, amount, chain
                )
            elif self.provider == "AAVE":
                return await self._request_aave_flash_loan(
                    token_address, amount, chain
                )
        except Exception as e:
            self.logger.error(f"Flash loan request failed: {e}")
            return None
    
    async def _request_balancer_flash_loan(
        self,
        token_address: str,
        amount: float,
        chain: str
    ) -> Optional[Dict]:
        """Request flash loan from Balancer V2 Vault."""
        # Implementation would use Balancer V2 Vault contract
        # flashLoan(recipient, tokens[], amounts[], userData)
        
        vault_address = self.config.BALANCER_V2_VAULT
        
        self.logger.info(f"Requesting Balancer flash loan from vault: {vault_address}")
        
        return {
            'provider': 'BALANCER',
            'vault': vault_address,
            'token': token_address,
            'amount': amount,
            'fee': self.calculate_flash_loan_fee(amount),
            'chain': chain,
            'status': 'PENDING'
        }
    
    async def _request_aave_flash_loan(
        self,
        token_address: str,
        amount: float,
        chain: str
    ) -> Optional[Dict]:
        """Request flash loan from Aave."""
        # Implementation would use Aave LendingPool contract
        # flashLoan(receiverAddress, assets[], amounts[], modes[], onBehalfOf, params, referralCode)
        
        self.logger.info("Requesting Aave flash loan")
        
        return {
            'provider': 'AAVE',
            'token': token_address,
            'amount': amount,
            'fee': self.calculate_flash_loan_fee(amount),
            'chain': chain,
            'status': 'PENDING'
        }
    
    def is_flash_loan_profitable(
        self,
        loan_amount: float,
        expected_profit: float
    ) -> tuple[bool, float]:
        """
        Check if using a flash loan is profitable.
        
        Args:
            loan_amount: Amount to borrow
            expected_profit: Expected profit from the trade
        
        Returns:
            Tuple of (is_profitable, net_profit)
        """
        fee = self.calculate_flash_loan_fee(loan_amount)
        net_profit = expected_profit - fee
        
        is_profitable = net_profit > 0
        
        self.logger.debug(
            f"Flash loan profitability: Gross profit ${expected_profit:.2f}, "
            f"Fee ${fee:.2f}, Net ${net_profit:.2f}"
        )
        
        return is_profitable, net_profit
    
    def get_max_loan_amount(self, pool_tvl: float, max_percent: float = 0.1) -> float:
        """
        Calculate maximum safe loan amount.
        
        Args:
            pool_tvl: Total value locked in the pool
            max_percent: Maximum percentage of TVL to borrow
        
        Returns:
            Maximum loan amount
        """
        return pool_tvl * max_percent
