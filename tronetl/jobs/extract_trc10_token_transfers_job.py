from tronetl.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl.jobs.base_job import BaseJob

from tronetl.mappers.rest.trc20_token_transfer_mapper import TokenTransferMapper
from tronetl.mappers.rest.log_mapper import LogMapper
from tronetl.mappers.rest.transaction_mapper import TronTransactionMapper
from tronetl.service.token_transfer_extractor import TokenTransferExtractor


class ExtractTrc10TokenTransfersJob(BaseJob):
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
        self.token_transfer_extractor = TokenTransferExtractor()
        self.transaction_mapper = TronTransactionMapper()
        self.log_mapper = LogMapper()

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(
            self.transactions_iterable, 
            self._extract_transfers
        )

    def _extract_transfers(self, transactions_list):
        for transaction_json in transactions_list:
            tx = self.transaction_mapper.json_dict_to_transaction(transaction_json)
            contract_address = tx.contract_address
            if tx.logs is not None and tx.logs is not [] and tx.result != False and contract_address != None:
                log_json_list = tx.logs
                log_list = []
                contract_address_list = []
                for idx, log_json in enumerate(log_json_list):
                    decimals = None
                    log = self.log_mapper.json_dict_to_log(log_json, transaction=tx, log_index=idx)
                    log_list.append(log)
                    contract_address_list.append(log.address)

                for log in log_list:
                    token_transfer = self.token_transfer_extractor.extract_transfer_from_log(log, decimals)
                    if token_transfer is not None:
                        self.item_exporter.export_item(self.token_transfer_mapper.token_transfer_to_dict(token_transfer))

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
