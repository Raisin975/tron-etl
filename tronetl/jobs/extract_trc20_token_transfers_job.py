from tronetl.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl.jobs.base_job import BaseJob

from tronetl.mappers.rest.token_transfer_mapper import TokenTransferMapper
from tronetl.mappers.rest.log_mapper import LogMapper
from tronetl.mappers.rest.transaction_mapper import TronTransactionMapper
from tronetl.service.trc20_token_transfer_extractor import Trc20TokenTransferExtractor


class ExtractTrc20TokenTransfersJob(BaseJob):
    def __init__(
            self,
            transactions_iterable,
            batch_size,
            max_workers,
            item_exporter
        ):
        self.transactions_iterable = transactions_iterable

        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self.item_exporter = item_exporter

        self.token_transfer_mapper = TokenTransferMapper()
        self.token_transfer_extractor = Trc20TokenTransferExtractor()
        self.transaction_mapper = TronTransactionMapper()
        self.log_mapper = LogMapper()

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(
            self.transactions_iterable, 
            self._extract_transfers
        )

    def _extract_transfers(self, transactions_json_list):
        tx_list = [self.transaction_mapper.json_dict_to_transaction(transaction_json) for transaction_json in transactions_json_list]

        for tx in tx_list:

            # a transaction with logs and contract_address is a transaction interacted with contract
            if tx.logs is not None and tx.logs != [] and tx.contract_address != None:
                log_list = [
                    self.log_mapper.json_dict_to_log(log_json, transaction=tx, log_index=idx) 
                    for idx, log_json in enumerate(tx.logs)
                ]
 
                for log in log_list:
                    token_transfer = self.token_transfer_extractor.extract_transfer_from_log(log, tx)
                    if token_transfer is not None:
                        self.item_exporter.export_item(self.token_transfer_mapper.token_transfer_to_dict(token_transfer))

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
