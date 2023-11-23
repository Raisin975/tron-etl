from tronetl.common.thread_local_proxy import ThreadLocalProxy
from tronetl.providers.auto import get_transaction_bundle_web3_provider_from_uri_list
from tronetl.jobs.exporters.transaction_item_exporter import transactions_item_exporter
from tronetl.jobs.export_blocks_and_transactions_job import ExtractBlocksAndTransactionJob
from blockchainetl.logging_utils import logging_basic_config

logging_basic_config()

GET_TRANSACTIONINFO_ENDPOINT = "/wallet/gettransactioninfobyblocknum"
GET_BLOCK_BY_NUM = "/wallet/getblockbynum"

"""export transations from transaction info and transactions."""
def export_blocks_and_transactions(
    start_block, end_block,
    rpc_url, 
    batch_size, max_workers, 
    transactions_output,
    block_output
):
    job = ExtractBlocksAndTransactionJob(
        start_block=start_block,
        end_block=end_block,
        batch_size=batch_size,
        max_workers=max_workers,
        transactions_batch_provider=ThreadLocalProxy(
            lambda: get_transaction_bundle_web3_provider_from_uri_list(
                uri_string_list=[rpc_url + GET_BLOCK_BY_NUM, rpc_url + GET_TRANSACTIONINFO_ENDPOINT], 
                method_list=["POST", "POST"]
            )
        ),
        item_exporter=transactions_item_exporter(
            transactions_output,
            block_output
        )
    )
    job.run()