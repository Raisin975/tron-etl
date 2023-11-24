class Trc20TokenTransfer(object):
    def __init__(self):
        self.token_address = None
        self.from_address = None
        self.to_address = None
        self.value = None
        self.tx_id = None
        self.log_index = None
        self.block_number = None
        self.result = None
        self.result_msg = None