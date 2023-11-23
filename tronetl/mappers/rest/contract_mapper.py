from tronetl.domain.rest.contract import TronContract


class TronContractMapper(object):
    
    def json_dict_to_contract(self, json_dict):
        contract = TronContract()
        contract.bytecode = json_dict.get('bytecode')
        contract.name = json_dict.get('name')
        contract.consume_user_resource_percent = json_dict.get('consume_user_resource_percent')
        contract.origin_address = json_dict.get('origin_address')
        contract.abi = [] if json_dict.get('abi') is None else json_dict.get('abi').get('entrys')
        contract.origin_energy_limit = json_dict.get('origin_energy_limit')
        contract.contract_address = json_dict.get('contract_address')
        contract.code_hash = json_dict.get('code_hash')
        return contract

    def contract_to_dict(self, contract):
        return {
            'type': 'contract',
            'bytecode': contract.bytecode,
            'name': contract.name,
            'consume_user_resource_percent': contract.consume_user_resource_percent,
            'origin_address': contract.origin_address,
            'abi': contract.abi,
            'origin_energy_limit': contract.origin_energy_limit,
            'contract_address': contract.contract_address,
            'code_hash': contract.code_hash,
        }