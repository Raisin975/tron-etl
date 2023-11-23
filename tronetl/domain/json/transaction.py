class JsonTransaction(object):
    def __init__(self):
        self.hash = None
        self.nonce = None
        self.block_hash = None
        self.block_number = None
        self.transaction_index = None
        self.from_address = None
        self.to_address = None
        self.value = None
        self.gas = None
        self.gas_price = None
        self.input = None
        self.max_fee_per_gas = None
        self.max_priority_fee_per_gas = None
        self.transaction_type = None