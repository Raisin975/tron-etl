from blockchainetl.jobs.exporters.composite_item_exporter import CompositeItemExporter

ASSET_FIELDS = [
    'asset_name',
    'token_id',
    'owner_address',
    'abbr',
    'total_supply',
    'trx_num',
    'num',
    'start_time',
    'end_time',
    'description',
    'url'
]


def asset_item_exporter(contract_output, converters=()):
    return CompositeItemExporter(
        filename_mapping={
            'asset': contract_output
        },
        field_mapping={
            'asset': ASSET_FIELDS
        },
        converters=converters
    )
