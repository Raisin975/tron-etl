from tronetl.domain.rest.block import TronBlock
from tronetl.mappers.rest.transaction_mapper import TronBlockTransactionMapper


class TronBlockMapper(object):
    
    def __init__(self, transaction_mapper=None):
        if transaction_mapper is None:
            self.transaction_mapper = TronBlockTransactionMapper()
        else:
            self.transaction_mapper = transaction_mapper

    def json_dict_to_block(self, json_dict):
        block = TronBlock()
        # print(json_dict)
        block.block_id = json_dict.get('blockID')
        block_header = json_dict.get('block_header')
        # print(block_header)
        raw_data = block_header.get('raw_data')
        block.block_number = raw_data.get('number')
        block.tx_trie_root = raw_data.get('txTrieRoot')
        block.witness_address = raw_data.get('witness_address')
        block.parent_hash = raw_data.get('parentHash')
        block.timestamp = raw_data.get('timestamp')
        block.witness_signature = block_header.get('witness_signature')

        if 'transactions' in json_dict:
            block.transactions = [
                self.transaction_mapper.json_dict_to_transaction(tx)
                for tx in json_dict['transactions']
                if isinstance(tx, dict)
            ]

            block.transaction_count = len(json_dict['transactions'])

        return block

    def block_to_dict(self, block):
        return {
            'type': 'block',
            'blockId': block.block_id,
            'blockNumber': block.block_number,
            'txTrieRoot': block.tx_trie_root,
            'witnessAddress': block.witness_address,
            'parentHash': block.parent_hash,
            'timestamp': block.timestamp,
            'witnessSignature': block.witness_signature,
            'transactionCount': block.transaction_count,
        }