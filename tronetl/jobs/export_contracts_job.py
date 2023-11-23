from tronetl.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl.jobs.base_job import BaseJob
from tronetl.mappers.rest.transaction_mapper import TronTransactionMapper
from tronetl.mappers.rest.contract_mapper import TronContractMapper
from tronetl.common.rest_rpc_requests import generate_contract_rest_rpc

class ExportContract(BaseJob):
    def __init__(
            self,
            transactions_iterable,
            batch_size, 
            max_workers,
            contract_provider,
            item_exporter
        ):
        self.transactions_iterable = transactions_iterable

        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self.contract_provider = contract_provider
        self.item_exporter = item_exporter

        self.contract_mapper = TronContractMapper()
        self.transaction_mapper = TronTransactionMapper()

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(
            self.transactions_iterable, 
            self._extract_transfers
        )

    def _extract_transfers(self, transactions_json_list):
        tx_list = [self.transaction_mapper.json_dict_to_transaction(transaction_json) for transaction_json in transactions_json_list]
        contract_address_list = []
        for tx in tx_list:
            if tx.contract_address is not None:
                contract_address_list.append(tx.contract_address)

        contracts_json_info = self.contract_provider.make_batch_request(list(generate_contract_rest_rpc(contract_address_list)))

        contracts = [self.contract_mapper.json_dict_to_contract(info) for info in contracts_json_info]
        for contract in contracts:
            self.item_exporter.export_item(self.contract_mapper.contract_to_dict(contract))

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
