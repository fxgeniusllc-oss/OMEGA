"""Constants and configuration for the DeFi Trading Bot."""

from typing import Dict, Any

# DEX Sources - 24 total across 4 chains
DEX_SOURCES: Dict[str, Dict[str, Dict[str, Any]]] = {
    "polygon": {
        "Uniswap V3": {
            "rpc_method": "uniswap_v3",
            "fee_tier": "0.01%",
            "liquidity_mult": 1.0,
            "router": "0xE592427A0AEce92De3Edee1F18E0157C05861564"
        },
        "QuickSwap": {
            "rpc_method": "quickswap",
            "fee_tier": "0.04%",
            "liquidity_mult": 0.95,
            "router": "0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff"
        },
        "Balancer": {
            "rpc_method": "balancer",
            "fee_tier": "0.03%",
            "liquidity_mult": 0.85,
            "vault": "0xBA12222222228d8Ba445958a75a0704d566BF2C8"
        },
        "SushiSwap": {
            "rpc_method": "sushiswap",
            "fee_tier": "0.03%",
            "liquidity_mult": 0.90,
            "router": "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506"
        },
        "Aave": {
            "rpc_method": "aave",
            "fee_tier": "0.09%",
            "liquidity_mult": 0.80,
            "pool": "0x794a61358D6845594F94dc1DB02A252b5b4814aD"
        }
    },
    "ethereum": {
        "Uniswap V3": {
            "rpc_method": "uniswap_v3",
            "fee_tier": "0.01%",
            "liquidity_mult": 1.0,
            "router": "0xE592427A0AEce92De3Edee1F18E0157C05861564"
        },
        "Uniswap V2": {
            "rpc_method": "uniswap_v2",
            "fee_tier": "0.03%",
            "liquidity_mult": 0.98,
            "router": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
        },
        "Curve Finance": {
            "rpc_method": "curve",
            "fee_tier": "0.04%",
            "liquidity_mult": 0.92,
            "router": "0x8e764bE4288B842791989DB5b8ec067279829809"
        },
        "Balancer": {
            "rpc_method": "balancer",
            "fee_tier": "0.03%",
            "liquidity_mult": 0.85,
            "vault": "0xBA12222222228d8Ba445958a75a0704d566BF2C8"
        },
        "SushiSwap": {
            "rpc_method": "sushiswap",
            "fee_tier": "0.03%",
            "liquidity_mult": 0.90,
            "router": "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F"
        },
        "1inch": {
            "rpc_method": "oneinch",
            "fee_tier": "0.02%",
            "liquidity_mult": 0.93,
            "router": "0x1111111254EEB25477B68fb85Ed929f73A960582"
        }
    },
    "arbitrum": {
        "Uniswap V3": {
            "rpc_method": "uniswap_v3",
            "fee_tier": "0.01%",
            "liquidity_mult": 1.0,
            "router": "0xE592427A0AEce92De3Edee1F18E0157C05861564"
        },
        "Camelot": {
            "rpc_method": "camelot",
            "fee_tier": "0.03%",
            "liquidity_mult": 0.88,
            "router": "0xc873fEcbd354f5A56E00E710B90EF4201db2448d"
        },
        "SushiSwap": {
            "rpc_method": "sushiswap",
            "fee_tier": "0.03%",
            "liquidity_mult": 0.90,
            "router": "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506"
        },
        "GMX": {
            "rpc_method": "gmx",
            "fee_tier": "0.10%",
            "liquidity_mult": 0.85,
            "router": "0xaBBc5F99639c9B6bCb58544ddf04EFA6802F4064"
        },
        "Balancer": {
            "rpc_method": "balancer",
            "fee_tier": "0.03%",
            "liquidity_mult": 0.85,
            "vault": "0xBA12222222228d8Ba445958a75a0704d566BF2C8"
        }
    },
    "optimism": {
        "Uniswap V3": {
            "rpc_method": "uniswap_v3",
            "fee_tier": "0.01%",
            "liquidity_mult": 1.0,
            "router": "0xE592427A0AEce92De3Edee1F18E0157C05861564"
        },
        "Curve Finance": {
            "rpc_method": "curve",
            "fee_tier": "0.04%",
            "liquidity_mult": 0.92,
            "router": "0x0DCCED1ABBED3a507920c16C6Fb661bF83A9f68e"
        },
        "SushiSwap": {
            "rpc_method": "sushiswap",
            "fee_tier": "0.03%",
            "liquidity_mult": 0.90,
            "router": "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506"
        },
        "Velodrome": {
            "rpc_method": "velodrome",
            "fee_tier": "0.02%",
            "liquidity_mult": 0.87,
            "router": "0xa062aE8A9c5e11aaA026fc2670B0D65cCc8B2858"
        }
    }
}

# Bridge Sources - 5 total
BRIDGE_SOURCES: Dict[str, Dict[str, Any]] = {
    "Stargate": {
        "fee": "0.06%",
        "router": "0x8731d54E9D02c286767d56ac03e8037C07e01e98",
        "chains": ["ethereum", "polygon", "arbitrum", "optimism"]
    },
    "Across": {
        "fee": "0.05%",
        "router": "0x5c7BCd6E7De5423a257D81B442095A1a6ced35C5",
        "chains": ["ethereum", "polygon", "arbitrum", "optimism"]
    },
    "Connext": {
        "fee": "0.05%",
        "router": "0x8898B472C54c31894e3B9bb83cEA802a5d0e63C6",
        "chains": ["ethereum", "polygon", "arbitrum", "optimism"]
    },
    "Hop Protocol": {
        "fee": "0.04%",
        "router": "0x3666f603Cc164936C1b87e207F36BEBa4AC5f18a",
        "chains": ["ethereum", "polygon", "arbitrum", "optimism"]
    },
    "Synapse": {
        "fee": "0.08%",
        "router": "0x2796317b0fF8538F253012862c06787Adfb8cEb6",
        "chains": ["ethereum", "polygon", "arbitrum", "optimism"]
    }
}

# CEX Sources - 3 total
CEX_SOURCES: Dict[str, Dict[str, Any]] = {
    "Binance": {
        "api_url": "https://api.binance.com/api/v3",
        "fee": "0.10%",
        "pairs": ["ETHUSDT", "BTCUSDT", "MATICUSDT"]
    },
    "Coinbase": {
        "api_url": "https://api.coinbase.com/v2",
        "fee": "0.50%",
        "pairs": ["ETH-USD", "BTC-USD", "MATIC-USD"]
    },
    "Kraken": {
        "api_url": "https://api.kraken.com/0/public",
        "fee": "0.26%",
        "pairs": ["ETHUSD", "BTCUSD", "MATICUSD"]
    }
}

# Token addresses by chain
TOKEN_ADDRESSES: Dict[str, Dict[str, str]] = {
    "polygon": {
        "WMATIC": "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
        "USDC": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
        "USDT": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
        "DAI": "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
        "WETH": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
        "WBTC": "0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6"
    },
    "ethereum": {
        "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
        "WBTC": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
    },
    "arbitrum": {
        "WETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        "USDC": "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8",
        "USDT": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
        "DAI": "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
        "WBTC": "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f"
    },
    "optimism": {
        "WETH": "0x4200000000000000000000000000000000000006",
        "USDC": "0x7F5c764cBc14f9669B88837ca1490cCa17c31607",
        "USDT": "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58",
        "DAI": "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
        "WBTC": "0x68f180fcCe6836688e9084f035309E29Bf0A2095"
    }
}

# Stablecoin addresses (for USD conversion)
STABLECOINS = ["USDC", "USDT", "DAI", "USD"]

# Chain IDs
CHAIN_IDS = {
    "ethereum": 1,
    "polygon": 137,
    "arbitrum": 42161,
    "optimism": 10
}
