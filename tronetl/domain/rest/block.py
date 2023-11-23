class TronBlock(object):
    def __init__(self):
        self.block_id = None
        self.block_number = None
        self.tx_trie_root = None
        self.parent_hash = None
        self.timestamp = None
        self.witness_address = None
        self.witness_signature = None
        self.transactions = []
        self.transaction_count = None