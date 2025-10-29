#!/usr/bin/env python3
"""
Example usage of the Transaction Engine

This script demonstrates how to:
1. Import and use the transaction engine
2. Configure for a specific network
3. Monitor the pipeline

For production use:
- Replace placeholder RPC URL
- Use secure key management
- Uncomment broadcast function
- Add real opportunity scanner
"""

import os
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src import transaction_engine

def main():
    """Run the transaction engine with example configuration"""
    
    print("=" * 60)
    print("OMEGA Transaction Engine - Example")
    print("=" * 60)
    print()
    print("⚠️  WARNING: This is a demonstration with placeholder data")
    print("⚠️  Broadcasting is DISABLED by default for safety")
    print()
    print("Configuration:")
    print("  - Network: Placeholder (update RPC URL)")
    print("  - Private Key: Placeholder (use secure storage)")
    print("  - Decision Engine: Always approves (stub)")
    print("  - Opportunities: Simulated data")
    print()
    print("Pipeline Status:")
    print("  [1] Opportunity Ingest   → Running")
    print("  [2] Decision Engine      → Running")
    print("  [3] Payload Encoder      → Running")
    print("  [4] Transaction Builder  → Running")
    print("  [5] Transaction Signer   → Running")
    print("  [6] Broadcast Engine     → Running (broadcasting disabled)")
    print()
    print("=" * 60)
    print("Starting transaction engine... Press Ctrl+C to stop")
    print("=" * 60)
    print()
    
    try:
        # Start the engine (runs indefinitely)
        transaction_engine.start_transaction_engine()
    except KeyboardInterrupt:
        print("\n")
        print("=" * 60)
        print("Shutting down transaction engine...")
        print(f"Final queue sizes:")
        print(f"  - Opportunities: {transaction_engine.opportunity_queue.qsize()}")
        print(f"  - Signed TXs: {transaction_engine.signed_tx_queue.qsize()}")
        print("=" * 60)
        sys.exit(0)

if __name__ == "__main__":
    main()
