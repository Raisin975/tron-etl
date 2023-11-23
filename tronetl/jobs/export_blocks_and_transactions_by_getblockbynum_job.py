from tronetl.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl.jobs.base_job import BaseJob
from tronetl.common.rest_rpc_requests import generate_get_block_by_num_rest_rpc
from tronetl.mappers.rest.transaction_mapper import TronBlockTransactionMapper
from tronetl.mappers.rest.block_mapper import TronBlockMapper
from tronetl.common.utils import rest_rpc_response_batch_to_results, validate_range


# Exports transactions
# /wallet/getblockbynum
class ExportBlocksAndTransactionsJob(BaseJob):
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
        
        self.block_mapper = TronBlockMapper()
        self.transaction_mapper = TronBlockTransactionMapper()

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(
            range(self.start_block, self.end_block + 1),
            self._export_batch,
            total_items=self.end_block - self.start_block + 1
        )

    def _export_batch(self, block_number_batch):
        blocks_rpc = list(generate_get_block_by_num_rest_rpc(block_number_batch))
        response = self.batch_web3_provider.make_batch_request(blocks_rpc)
        json_blocks = rest_rpc_response_batch_to_results(response)
        blocks = [self.block_mapper.json_dict_to_block(blk) for blk in json_blocks]

        for blk in blocks:
            self._export_block_and_transactions(blk)

    def _export_block_and_transactions(self, block):
        self.item_exporter.export_item(self.block_mapper.block_to_dict(block))
        for tx in block.transactions:
            self.item_exporter.export_item(self.transaction_mapper.transaction_to_dict(tx))

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()

