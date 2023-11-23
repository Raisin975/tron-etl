# TRON-ETL

- TRON RESTFULL API does not support batch request 
- Batch requests are a feature of the Ethereum JSON-RPC API that allows multiple requests to be sent in a single HTTP POST request

## Quickstart
Clone Tron ETL:

```bash
git clone https://github.com/Raisin975/tron-etl.git
```

Export Transactions and Blocks
```python
export_blocks_and_transactions(
    start_block, end_block, 
    rpc_url=rpc_url,
    batch_size=batch_size, 
    max_workers=max_worker, 
    transactions_output=data_save_path + "/transactions.json",
    block_output=data_save_path + "/blocks.json"
)
```

Export TRC20 Transfers
```python
extract_trc20_token_transfers(
    transactions=data_save_path + "/transactions.json",
    batch_size=batch_size, 
    max_workers=max_worker, 
    output=data_save_path + "/trc20_transfers.json"
)
```

Export TRC10 Transfers
```python
extract_trc10_token_transfers(
    transactions=data_save_path + "/transactions.json",
    batch_size=batch_size, 
    max_workers=max_worker, 
    output=data_save_path + "/trc10_transfers.json"
)
```

Export Contracts
```python
export_contracts(
    transactions=data_save_path + "/transactions.json",
    rpc_url=rpc_url,
    batch_size=batch_size, 
    max_workers=max_worker, 
    output=data_save_path + "/contracts.json"
)
```

## Running in Docker
coding...