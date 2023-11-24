from tronetl.jobs.export_blocks_job import ExportBlocksJob
from tronetl.jobs.exporters.block_and_transaction_item_exporter import blocks_and_transactions_item_exporter_by_restrpc
from blockchainetl.logging_utils import logging_basic_config
from tronetl.providers.auto import get_rest_provider_from_uri
from tronetl.common.thread_local_proxy import ThreadLocalProxy


logging_basic_config()

GET_BLOCK_BY_NUM = "/wallet/getblockbynum"

def export_blocks(
    start_block, end_block, batch_size, provider_uri, 
    max_workers, 
    blocks_ouput, transactions_output
):
    job = ExportBlocksJob(
        start_block=start_block,
        end_block=end_block,
        batch_size=batch_size,
        batch_web3_provider=ThreadLocalProxy(lambda: get_rest_provider_from_uri(
            provider_uri + GET_BLOCK_BY_NUM, method="POST"
        )),
        max_workers=max_workers,
        item_exporter=blocks_and_transactions_item_exporter_by_restrpc(blocks_ouput, transactions_output)
    )
    job.run()
