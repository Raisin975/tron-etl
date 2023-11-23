import json

from blockchainetl.file_utils import smart_open
from blockchainetl.jobs.exporters.converters.int_to_string_item_converter import IntToStringItemConverter
from tronetl.jobs.exporters.contract_item_exporter import contract_item_exporter
from tronetl.providers.auto import get_rest_provider_from_uri
from tronetl.common.thread_local_proxy import ThreadLocalProxy
from tronetl.jobs.export_contract_job import ExportContract
from blockchainetl.logging_utils import logging_basic_config

logging_basic_config()

GET_CONTRACT = '/wallet/getcontract'

def export_contracts(
    contract_addresses, rpc_url,
    batch_size, max_workers, 
    output, values_as_strings=False
):
    with smart_open(contract_addresses, 'r') as contracts_file:
        if contract_addresses.endswith('.json'):
            contract_addresses_reader = (
                contract_address.strip() for contract_address in contracts_file
                if contract_address.strip()
            )
        else:
            return 
        converters = [IntToStringItemConverter(keys=['value'])] if values_as_strings else []
        job = ExportContract(
            contracts_iterable=contract_addresses_reader,
            batch_size=batch_size,
            max_workers=max_workers,
            contract_provider=ThreadLocalProxy(lambda : get_rest_provider_from_uri(
                rpc_url + GET_CONTRACT,
                'POST'
            )),
            item_exporter=contract_item_exporter(output, converters=converters)
        )
        job.run()

