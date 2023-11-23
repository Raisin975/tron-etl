from tronetl.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl.jobs.base_job import BaseJob

from tronetl.common.rest_rpc_requests import generate_transaction_rest_rpc
from tronetl.mappers.rest.transaction_mapper import TronTransactionInfoMapper, TronTransactionMapper
from tronetl.mappers.rest.block_mapper import TronBlockMapper

from tronetl.service.transaction_extractor import TransactionExtractor

# Extract transactions
class ExtractBlocksAndTransactionJob(BaseJob):
    def __init__(
            self,
            start_block, end_block,
            batch_size,
            max_workers,
            transactions_batch_provider,
            item_exporter
        ):
        self.start_block = start_block
        self.end_block = end_block
        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self.item_exporter = item_exporter
        self.batch_web3_provider = transactions_batch_provider

        self.block_mapper = TronBlockMapper()

        self.transaction_extractor = TransactionExtractor()
        self.transaction_mapper = TronTransactionMapper()
        self.transaction_info_mapper = TronTransactionInfoMapper()
        

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(
            range(self.start_block, self.end_block + 1),
            self._export_batch,
            total_items=self.end_block - self.start_block + 1
        )

    def _export_batch(self, batch_transations):
        blocks_rpc = list(generate_transaction_rest_rpc(batch_transations))
        block_and_transactions = self.batch_web3_provider.make_batch_request(blocks_rpc)

        for block_and_transaction_info in block_and_transactions:
            blk = block_and_transaction_info[0]
            blk = self.block_mapper.json_dict_to_block(blk)
            block_transactions = blk.transactions
            self._export_block(blk)
            
            transactions_info = [] 
            tx_info = block_and_transaction_info[1]
            # print(tx_info)
            for tx in tx_info:
                transactions_info.append(self.transaction_info_mapper.json_dict_to_transaction(tx))
            
            self._export_transactions(block_transactions, transactions_info, blk)
            
    def _export_transactions(self, block_transactions, transactions_info, blk):
        for idx, blk_tx in enumerate(block_transactions):
            tx_info = transactions_info[idx]
            assert(tx_info.id_ == blk_tx.txID)
            tx = self.transaction_extractor.extract_transaction(blk_tx, tx_info, blk, idx)
            self.item_exporter.export_item(self.transaction_mapper.transaction_to_dict(tx))

    def _export_block(self, block):
        self.item_exporter.export_item(self.block_mapper.block_to_dict(block))
            
    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()

