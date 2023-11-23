import json

from blockchainetl.file_utils import smart_open
from blockchainetl.jobs.exporters.converters.int_to_string_item_converter import IntToStringItemConverter
from tronetl.jobs.exporters.token_transfer_item_exporter import trc10_token_transfers_item_exporter
from tronetl.providers.auto import get_rest_provider_from_uri
from tronetl.common.thread_local_proxy import ThreadLocalProxy
from tronetl.jobs.extract_trc10_token_transfers_job import ExtractTrc10TokenTransfersJob
from blockchainetl.logging_utils import logging_basic_config

logging_basic_config()

GET_CONTRACT = '/wallet/getcontract'

"""Extracts ERC20/ERC721 transfers from logs file."""
def extract_trc10_token_transfers(
    transactions, rpc_url,
    batch_size, max_workers, 
    output, values_as_strings=False
):
    with smart_open(transactions, 'r') as transactions_file:
        if transactions.endswith('.json'):
            transactions_reader = (json.loads(line) for line in transactions_file)
        else:
            return 
        converters = [IntToStringItemConverter(keys=['value'])] if values_as_strings else []
        job = ExtractTrc10TokenTransfersJob(
            transactions_iterable=transactions_reader,
            batch_size=batch_size,
            max_workers=max_workers,
            fullnode_rpc=rpc_url,
            decimal_provider=ThreadLocalProxy(lambda : get_rest_provider_from_uri(
                rpc_url + GET_CONTRACT,
                'POST'
            )),
            item_exporter=trc10_token_transfers_item_exporter(output, converters=converters)
        )
        job.run()

