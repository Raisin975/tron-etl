from blockchainetl.jobs.exporters.composite_item_exporter import CompositeItemExporter

CONTRACT_FIELDS = [
    'bytecode',
    'name',
    'consume_user_resource_percent',
    'origin_address',
    'abi',
    'origin_energy_limit',
    'contract_address',
    'code_hash'
]


def contract_item_exporter(contract_output, converters=()):
    return CompositeItemExporter(
        filename_mapping={
            'contract': contract_output
        },
        field_mapping={
            'contract': CONTRACT_FIELDS
        },
        converters=converters
    )
