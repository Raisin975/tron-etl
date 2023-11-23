class TronContract(object):
    def __init__(self):
        self.bytecode = None
        self.name = None
        self.consume_user_resource_percent = None
        self.origin_address = None
        self.abi = None # ['abi']['entrys']
        self.origin_energy_limit = None
        self.contract_address = None
        self.code_hash = None