from tronetl.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl.jobs.base_job import BaseJob
from tronetl.common.rest_rpc_requests import generate_get_txinfo_by_blocknumber_rest_rpc
from tronetl.mappers.rest.transaction_mapper import TronTransactionInfoMapper
from tronetl.common.utils import rest_rpc_response_batch_to_results, validate_range


# Exports transactions info 
# /wallet/gettransactioninfobyblocknum
class ExportTransactionsJob(BaseJob):
    def __init__(
            self,
            start_block,
            end_block,
            batch_size,
            batch_web3_provider,
            max_workers,
            item_exporter):
        validate_range(start_block, end_block)
        self.start_block = start_block
        self.end_block = end_block

        self.batch_web3_provider = batch_web3_provider

        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self.item_exporter = item_exporter

        self.transaction_mapper = TronTransactionInfoMapper()

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(
            range(self.start_block, self.end_block + 1),
            self._export_batch,
            total_items=self.end_block - self.start_block + 1
        )

    def _export_batch(self, block_number_batch):
        blocks_rpc = list(generate_get_txinfo_by_blocknumber_rest_rpc(block_number_batch))
        response = self.batch_web3_provider.make_batch_request(blocks_rpc)
        json_blocks_transactions = rest_rpc_response_batch_to_results(response)
        blocks = []
        for block_transactions in json_blocks_transactions:
            transactions = []
            for json_tx in block_transactions:
                transactions.append(self.transaction_mapper.json_dict_to_transaction(json_tx))
            blocks.append(transactions)
        for transactions in blocks:
            self._export_transactions(transactions)

    def _export_transactions(self, block_transactions):
        for tx in block_transactions:
            self.item_exporter.export_item(self.transaction_mapper.transaction_to_dict(tx))

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()

