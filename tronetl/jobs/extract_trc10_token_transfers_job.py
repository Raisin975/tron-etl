from tronetl.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl.jobs.base_job import BaseJob

from tronetl.mappers.rest.trc10_token_transfer_mapper import Trc10TokenTransferMapper
from tronetl.mappers.rest.log_mapper import LogMapper
from tronetl.mappers.rest.transaction_mapper import TronTransactionMapper
from tronetl.service.trc10_token_transfer_extractor import Trc10TokenTransferExtractor


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

        self.token_transfer_mapper = Trc10TokenTransferMapper()
        self.token_transfer_extractor = Trc10TokenTransferExtractor()
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

        contract_parameter_value_list = [
            (tx, tx.contract[0]['parameter']['value'])            
            for tx in tx_list
            if tx.contract_address == None and 'asset_name' in tx.contract[0]['parameter']['value'].keys()
        ]
        
        for tx_and_contract_parameter_value in contract_parameter_value_list:
            token_transfer = self.token_transfer_extractor.extract_transfer_from_contract_and_tx(tx_and_contract_parameter_value)
            self.item_exporter.export_item(self.token_transfer_mapper.token_transfer_to_dict(token_transfer))

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
