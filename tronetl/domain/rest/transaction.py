class TronTransactionInfo(object):
    """
        wallet/gettransactioninfobyid
    """
    def __init__(self):
        self.id_ = None
        self.block_number = None
        self.block_timestamp = None
        self.contract_address = None
        self.contract_result = None
        self.fee = None
        self.receipt = None
        self.log = []
        self.internal_transactions = None


class TronBlockTransaction(object):
    """
        wallet/gettransactionbyid
    """
    def __init__(self):
        self.ret = []
        self.signature = []
        self.txID = None
        self.raw_data = None
        self.raw_data_hex = None


class TronTransaction(object):
    """
        transactions
        /wallet/gettransactionbyid
        /wallet/gettransactioninfobyid
    """
    def __init__(self):
        self.tx_index = None
        # /wallet/gettransactioninfobyid
        self.tx_id = None
        self.block_id = None
        self.block_number = None
        self.block_timestamp = None
        self.fee = None # trx consumed
        self.contract_result = []
        self.contract_address = None
        # receipt 
        # self.receipt = None
        self.result = None # it appeats when transaction emit error
        self.result_msg = None # it appeats when transaction emit error
        self.receipt_result = None # receipt result / contract ret
        self.net_usage = None # receipt: bandwidth usage
        self.net_fee = None # receipt: burned trx for bandwidth
        self.energy_fee = None # receipt: burned trx for energy
        self.energy_usage_total = None # receipt: total usage energy
        self.energy_penalty_total = None
        self.logs = []
        self.internal_transactions = []

        # /wallet/gettransactionbyid
        self.ret = []
        self.signature = []
        self.contract = [] # inclue trc10/trx information or contract input data
        self.ref_block_bytes = None
        self.ref_block_hash = None
        self.expiration = None
        self.fee_limit = None
        self.timestamp = None
        self.raw_data_hex = None