"""Strategies package initialization."""
from .base import BaseStrategy
from .mempool import MempoolWatcher
from .arbitrage import CrossChainArbitrageur
from .bridge import BridgeArbitrageur
from .pump_prediction import PumpPredictionAI
from .market_making import MarketMaker
from .statistical_arbitrage import StatisticalArbitrageur
from .gamma_scalping import GammaScalper
from .funding_rate import FundingRateHarvester
from .volatility_arbitrage import VolatilityArbitrageur

__all__ = [
    'BaseStrategy',
    'MempoolWatcher',
    'CrossChainArbitrageur',
    'BridgeArbitrageur',
    'PumpPredictionAI',
    'MarketMaker',
    'StatisticalArbitrageur',
    'GammaScalper',
    'FundingRateHarvester',
    'VolatilityArbitrageur',
]
