from tronetl.jobs.exporters.json.export_blocks_and_transactions_job import ExportBlocksAndTransactionsJob
from tronetl.jobs.exporters.block_and_transaction_item_exporter import blocks_and_transactions_item_exporter_by_jsonrpc
from blockchainetl.logging_utils import logging_basic_config
from tronetl.providers.auto import get_json_provider_from_uri
from tronetl.common.thread_local_proxy import ThreadLocalProxy


logging_basic_config()

def export_blocks_and_transactions(start_block, end_block, batch_size, provider_uri, max_workers, 
                                   blocks_output, transactions_output):
    """Exports blocks and transactions."""
    if blocks_output is None and transactions_output is None:
        raise ValueError('Either --blocks-output or --transactions-output options must be provided')

    job = ExportBlocksAndTransactionsJob(
        start_block=start_block,
        end_block=end_block,
        batch_size=batch_size,
        batch_web3_provider=ThreadLocalProxy(lambda: get_json_provider_from_uri(provider_uri, batch=True)),
        max_workers=max_workers,
        item_exporter=blocks_and_transactions_item_exporter_by_jsonrpc(blocks_output, transactions_output),
        export_blocks=blocks_output is not None,
        export_transactions=transactions_output is not None)
    job.run()