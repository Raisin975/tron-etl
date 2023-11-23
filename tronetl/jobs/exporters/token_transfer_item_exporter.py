from blockchainetl.jobs.exporters.composite_item_exporter import CompositeItemExporter

FIELDS_TO_EXPORT = [
    'token_address',
    'from_address',
    'to_address',
    'value',
    'tx_id',
    'log_index',
    'block_number',
    'decimals'
]


def token_transfers_item_exporter(token_transfer_output, converters=()):
    return CompositeItemExporter(
        filename_mapping={
            'token_transfer': token_transfer_output
        },
        field_mapping={
            'token_transfer': FIELDS_TO_EXPORT
        },
        converters=converters
    )
