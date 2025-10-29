"""Position manager for risk management."""
from typing import Dict, Optional
from src.utils.helpers import calculate_position_size, calculate_kelly_fraction


class PositionManager:
    """Manages positions and enforces Kelly Criterion sizing and risk limits."""
    
    def __init__(self, config, logger):
        """Initialize position manager."""
        self.config = config
        self.logger = logger
        self.positions: Dict[str, Dict] = {}
        self.total_capital = 0.0
        self.used_capital = 0.0
    
    def update_capital(self, total_capital: float):
        """Update total available capital."""
        self.total_capital = total_capital
        self.logger.info(f"Capital updated: ${total_capital:.2f}")
    
    def calculate_position_size(
        self,
        strategy_name: str,
        win_probability: float,
        expected_profit: float,
        expected_loss: float
    ) -> float:
        """
        Calculate optimal position size using Kelly Criterion.
        
        Args:
            strategy_name: Name of the strategy
            win_probability: Probability of success (0-1)
            expected_profit: Expected profit in USD
            expected_loss: Expected loss in USD
        
        Returns:
            Recommended position size in USD
        """
        available_capital = self.total_capital - self.used_capital
        
        position_size = calculate_position_size(
            capital=available_capital,
            win_probability=win_probability,
            expected_profit=expected_profit,
            expected_loss=expected_loss,
            max_position=self.config.MAX_POSITION_SIZE
        )
        
        # Apply risk per trade limit
        max_risk_amount = self.total_capital * self.config.RISK_PER_TRADE
        position_size = min(position_size, max_risk_amount / expected_loss * expected_profit)
        
        self.logger.info(
            f"Position size calculated for {strategy_name}: "
            f"${position_size:.2f} (Win prob: {win_probability:.2%})"
        )
        
        return position_size
    
    def can_open_position(self, amount: float) -> bool:
        """Check if a position can be opened."""
        available_capital = self.total_capital - self.used_capital
        
        if amount > available_capital:
            self.logger.warning(
                f"Insufficient capital: Required ${amount:.2f}, "
                f"Available ${available_capital:.2f}"
            )
            return False
        
        if amount > self.config.MAX_POSITION_SIZE:
            self.logger.warning(
                f"Position size ${amount:.2f} exceeds max ${self.config.MAX_POSITION_SIZE:.2f}"
            )
            return False
        
        return True
    
    def open_position(
        self,
        position_id: str,
        strategy_name: str,
        amount: float,
        entry_price: float,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Open a new position.
        
        Args:
            position_id: Unique position identifier
            strategy_name: Strategy name
            amount: Position amount in USD
            entry_price: Entry price
            metadata: Additional position metadata
        
        Returns:
            True if position opened successfully
        """
        if not self.can_open_position(amount):
            return False
        
        self.positions[position_id] = {
            'strategy': strategy_name,
            'amount': amount,
            'entry_price': entry_price,
            'metadata': metadata or {},
            'status': 'OPEN'
        }
        
        self.used_capital += amount
        
        self.logger.info(
            f"Position opened: {position_id} | {strategy_name} | "
            f"${amount:.2f} @ {entry_price:.6f}"
        )
        
        return True
    
    def close_position(
        self,
        position_id: str,
        exit_price: float,
        profit_loss: float
    ) -> bool:
        """
        Close an existing position.
        
        Args:
            position_id: Position identifier
            exit_price: Exit price
            profit_loss: Realized profit/loss
        
        Returns:
            True if position closed successfully
        """
        if position_id not in self.positions:
            self.logger.warning(f"Position not found: {position_id}")
            return False
        
        position = self.positions[position_id]
        position['status'] = 'CLOSED'
        position['exit_price'] = exit_price
        position['profit_loss'] = profit_loss
        
        self.used_capital -= position['amount']
        self.total_capital += profit_loss
        
        self.logger.info(
            f"Position closed: {position_id} | {position['strategy']} | "
            f"P&L: ${profit_loss:.2f}"
        )
        
        return True
    
    def get_position_info(self, position_id: str) -> Optional[Dict]:
        """Get information about a specific position."""
        return self.positions.get(position_id)
    
    def get_open_positions(self) -> Dict[str, Dict]:
        """Get all open positions."""
        return {
            pid: pos for pid, pos in self.positions.items()
            if pos['status'] == 'OPEN'
        }
    
    def get_utilization(self) -> float:
        """Get capital utilization as a percentage."""
        if self.total_capital <= 0:
            return 0.0
        return (self.used_capital / self.total_capital) * 100
    
    def get_risk_metrics(self) -> Dict:
        """Get current risk metrics."""
        return {
            'total_capital': self.total_capital,
            'used_capital': self.used_capital,
            'available_capital': self.total_capital - self.used_capital,
            'utilization_pct': self.get_utilization(),
            'open_positions': len(self.get_open_positions()),
            'max_position_size': self.config.MAX_POSITION_SIZE,
            'risk_per_trade': self.config.RISK_PER_TRADE,
        }
