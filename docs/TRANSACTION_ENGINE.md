# Transaction Engine Documentation

## Overview

The Hyper-Compact Transaction Engine is a modular, high-performance system for processing blockchain transactions. It consists of six core modules that work together in a pipeline architecture.

## Architecture

### Pipeline Flow

```
Opportunity Ingest → Decision Engine → Payload Encoder → Transaction Builder → Signer → Broadcast Engine
```

### Modules

#### Module 1: Opportunity Ingest
- **Function**: `ingest_opportunities()`
- **Purpose**: Continuously fetches/selects trading opportunities from scanners or scorers
- **Output**: Adds opportunities to `opportunity_queue`
- **Status**: Currently uses placeholder data; integrate with real opportunity scanner

#### Module 2: Payload Encoder
- **Function**: `encode_payload(opportunity)`
- **Purpose**: Encodes function calls into ABI-compliant bytecode
- **Input**: Opportunity dict with contract address, method, and arguments
- **Output**: Encoded transaction data (bytes)
- **Note**: Uses example ABI; replace with actual contract ABIs in production

#### Module 3: Transaction Builder
- **Function**: `build_transaction(opportunity, data)`
- **Purpose**: Constructs a complete transaction object with all required fields
- **Input**: Opportunity dict and encoded data
- **Output**: Transaction dict with gas, nonce, gasPrice, etc.
- **Customizable**: Gas limits, gas prices, chain IDs

#### Module 4: Transaction Signer
- **Function**: `sign_transaction(tx)`
- **Purpose**: Signs transactions with the private key
- **Input**: Transaction dict
- **Output**: Signed transaction object
- **Security**: Private key should be loaded from secure storage (env vars, hardware wallet, etc.)

#### Module 5: Broadcast Engine
- **Function**: `broadcast_engine()`
- **Purpose**: Monitors signed transaction queue and broadcasts to blockchain
- **Input**: Reads from `signed_tx_queue`
- **Output**: Submits transactions to blockchain (currently disabled for safety)
- **Note**: `send_raw_transaction` call is commented out for security/compliance

#### Module 6: ML Decision Engine
- **Function**: `decision_engine(opportunity)`
- **Purpose**: Evaluates opportunities using ML models or logic
- **Input**: Opportunity dict
- **Output**: Boolean (approve/reject)
- **Status**: Stub implementation (always approves); integrate ML models as needed

### Pipeline Worker

The `pipeline_worker()` function orchestrates the flow:
1. Polls `opportunity_queue`
2. Runs opportunities through decision engine
3. Encodes approved opportunities
4. Builds and signs transactions
5. Adds signed transactions to `signed_tx_queue`

## Usage

### Basic Usage

```python
from src.transaction_engine import start_transaction_engine

# Start the engine (runs indefinitely)
start_transaction_engine()
```

### Running as Script

```bash
python -m src.transaction_engine
```

### Configuration

Before running, configure:

1. **RPC Endpoint**: Replace `"https://your-node-url"` with your actual node URL
2. **Private Key**: Set `PRIVATE_KEY` environment variable or use secure key management
3. **Chain ID**: Update `chainId` in `build_transaction()` for your target network
4. **Gas Parameters**: Adjust gas limit and gas price based on network conditions

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
# Edit .env with your configuration
```

Key variables:
- `PRIVATE_KEY`: Your wallet's private key
- `ETHEREUM_RPC_URL`: Your Ethereum node endpoint
- `POLYGON_RPC_URL`: Your Polygon node endpoint
- Other chain-specific RPC URLs

## Safety Features

### Security Considerations

1. **Transaction Broadcasting Disabled**: The `send_raw_transaction` call is commented out by default
2. **Placeholder Data**: Uses fake contract addresses and data by default
3. **Environment-based Config**: Private keys should be externalized
4. **Decision Gate**: All opportunities pass through decision engine before execution

### Enabling Live Execution

⚠️ **WARNING**: Only enable after thorough testing

To enable live broadcasting:
1. Uncomment the `send_raw_transaction` call in the `broadcast_engine()` function
2. Ensure all configurations are correct
3. Test on testnet first
4. Start with small amounts

## Performance Characteristics

- **Threading**: Uses Python threads for concurrent processing
- **Queues**: In-memory queue.Queue for pipeline communication
- **Status Monitoring**: Logs queue sizes every 5 seconds
- **Simulated Delay**: 0.1s between opportunity ingestion (configurable)

## Extending the Engine

### Adding Custom Decision Logic

Replace the stub in `decision_engine()`:

```python
def decision_engine(opportunity):
    # Your custom logic here
    if opportunity['value'] < minimum_threshold:
        return False
    
    # Call ML model
    prediction = ml_model.predict(opportunity)
    return prediction > confidence_threshold
```

### Integrating Real Opportunity Scanner

Update `ingest_opportunities()`:

```python
def ingest_opportunities():
    scanner = OpportunityScanner()
    while True:
        opportunities = scanner.scan()
        for opp in opportunities:
            opportunity_queue.put(opp)
        time.sleep(scan_interval)
```

### Adding Metrics/Monitoring

Add logging or metrics collection:

```python
import logging

def broadcast_engine():
    while True:
        if not signed_tx_queue.empty():
            signed_tx = signed_tx_queue.get()
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            logging.info(f"TX broadcasted: {tx_hash.hex()}")
            # metrics.increment('transactions.sent')
```

## Testing

Run the test suite:

```bash
pytest tests/test_transaction_engine.py -v
```

Tests cover:
- Decision engine logic
- Queue initialization
- Transaction building
- Payload encoding (with mocks)
- Transaction signing (with mocks)

## Troubleshooting

### Common Issues

1. **Web3 Connection Error**
   - Verify RPC endpoint is accessible
   - Check network connectivity
   - Ensure endpoint supports required methods

2. **Invalid Private Key**
   - Ensure private key is in correct format (hex string without 0x prefix)
   - Never commit private keys to version control

3. **Transaction Fails**
   - Check gas limits are sufficient
   - Verify gas price is competitive
   - Ensure account has sufficient balance
   - Validate contract address and ABI

4. **Nonce Issues**
   - Clear pending transactions
   - Ensure only one instance is running
   - Consider implementing nonce management

## Dependencies

See `requirements.txt` for full list. Key dependencies:

- `web3>=6.11.3`: Ethereum/blockchain interaction
- `eth-account>=0.10.0`: Transaction signing
- Python 3.8+: Required for type hints and async features

## License

See repository LICENSE file.

## Support

For issues and questions, please open an issue on the GitHub repository.
