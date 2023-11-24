from tronetl.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl.jobs.base_job import BaseJob
from tronetl.mappers.rest.transaction_mapper import TronTransactionMapper
from tronetl.mappers.rest.contract_mapper import TronContractMapper
from tronetl.common.rest_rpc_requests import generate_contract_rest_rpc


class ExportContract(BaseJob):
    def __init__(
            self,
            contracts_iterable,
            batch_size, 
            max_workers,
            contract_provider,
            item_exporter
        ):
        self.contracts_iterable = contracts_iterable

        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self.contract_provider = contract_provider
        self.item_exporter = item_exporter

        self.contract_mapper = TronContractMapper()
        self.transaction_mapper = TronTransactionMapper()

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(
            self.contracts_iterable, 
            self._extract_contracts
        )

    def _extract_contracts(self, contract_addresses_list):
        # contracts_json_info = self.contract_provider.make_batch_request(list(generate_contract_rest_rpc(contract_addresses_list)))

        # contracts = [self.contract_mapper.json_dict_to_contract(info) for info in contracts_json_info]
        # for contract in contracts:
        #     self.item_exporter.export_item(self.contract_mapper.contract_to_dict(contract))
        pass

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
