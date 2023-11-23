import json

from blockchainetl.file_utils import smart_open
from blockchainetl.jobs.exporters.converters.int_to_string_item_converter import IntToStringItemConverter
from tronetl.jobs.exporters.token_transfer_item_exporter import trc20_token_transfers_item_exporter
from tronetl.jobs.extract_trc20_token_transfers_job import ExtractTrc20TokenTransfersJob
from blockchainetl.logging_utils import logging_basic_config

logging_basic_config()

GET_CONTRACT = '/wallet/getcontract'

"""
    Extracts ERC20 transfers from logs file.
    Not include ERC721 transfer
"""
def extract_trc20_token_transfers(
    transactions,
    batch_size, max_workers, 
    output, values_as_strings=False
):
    with smart_open(transactions, 'r') as transactions_file:
        if transactions.endswith('.json'):
            transactions_reader = (json.loads(line) for line in transactions_file)
        else:
            return 
        converters = [IntToStringItemConverter(keys=['value'])] if values_as_strings else []
        job = ExtractTrc20TokenTransfersJob(
            transactions_iterable=transactions_reader,
            batch_size=batch_size,
            max_workers=max_workers,
            item_exporter=trc20_token_transfers_item_exporter(output, converters=converters)
        )
        job.run()

