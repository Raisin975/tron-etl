from blockchainetl.jobs.exporters.composite_item_exporter import CompositeItemExporter

TRC20_FIELDS = [
    'token_address',
    'from_address',
    'to_address',
    'value',
    'tx_id',
    'log_index',
    'block_number',
    'result',
    'result_msg'
]

TRC10_FIELDS = [
    
]

def trc20_token_transfers_item_exporter(token_transfer_output, converters=()):
    return CompositeItemExporter(
        filename_mapping={
            'trc20_token_transfer': token_transfer_output
        },
        field_mapping={
            'trc20_token_transfer': TRC20_FIELDS
        },
        converters=converters
    )


def trc10_token_transfers_item_exporter(token_transfer_output, converters=()):
    return CompositeItemExporter(
        filename_mapping={
            'trc10_token_transfer': token_transfer_output
        },
        field_mapping={
            'trc10_token_transfer': TRC20_FIELDS
        },
        converters=converters
    )