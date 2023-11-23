from tronetl.jobs.export_transactions_info_job import ExportTransactionsJob
from tronetl.jobs.exporters.block_and_transaction_item_exporter import transactions_info_item_exporter_by_restrpc
from blockchainetl.logging_utils import logging_basic_config
from tronetl.providers.auto import get_rest_provider_from_uri
from tronetl.common.thread_local_proxy import ThreadLocalProxy


logging_basic_config()

GET_TRANSACTIONINFO_ENDPOINT = "/wallet/gettransactioninfobyblocknum"

def export_transactions_info(
    start_block, end_block, batch_size, provider_uri, 
    max_workers, 
    transactions_output
):
    job = ExportTransactionsJob(
        start_block=start_block,
        end_block=end_block,
        batch_size=batch_size,
        batch_web3_provider=ThreadLocalProxy(lambda: get_rest_provider_from_uri(
            provider_uri + GET_TRANSACTIONINFO_ENDPOINT, method="POST"
        )),
        max_workers=max_workers,
        item_exporter=transactions_info_item_exporter_by_restrpc(transactions_output)
    )
    job.run()
