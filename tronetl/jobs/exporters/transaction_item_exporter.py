from blockchainetl.jobs.exporters.composite_item_exporter import CompositeItemExporter

TRANSACTION_DETAILS_FIELDS_TO_EXPORT = [
    'tx_id',
    'tx_index',
    'block_id',
    'block_number',
    'block_timestamp',
    'fee',
    'contract_result',
    'ret',
    'result',
    'result_msg',
    'receipt_result',
    'net_usage',
    'net_fee',
    'energy_fee',
    'energy_usage_total',
    'energy_penalty_total',
    'contract_address',
    'logs',
    'internal_transactions',
    'signature',
    'contract',
    'ref_block_bytes',
    'ref_block_hash',
    'expiration',
    'fee_limit',
    'timestamp',
    'raw_data_hex'
]

BLOCK_FIELDS_TO_EXPORT = [
    'blockId',
    'blockNumber',
    'txTrieRoot',
    'witnessAddress',
    'parentHash',
    'timestamp',
    'witnessSignature',
    'transactionCount'
]

def transactions_item_exporter(
    transactions_output=None,
    block_output=None, 
    converters=None
):
    return CompositeItemExporter(
        filename_mapping={
            'transaction': transactions_output,
            'block': block_output
        },
        field_mapping={
            'transaction': TRANSACTION_DETAILS_FIELDS_TO_EXPORT,
            'block': BLOCK_FIELDS_TO_EXPORT
        },
        converters=converters
    )
