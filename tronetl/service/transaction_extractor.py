from tronetl.domain.rest.transaction import TronTransaction
from tronetl.common.utils import hex_to_words

class TransactionExtractor(object):
    
    def extract_transaction(self, blk_tx, tx_info, blk, tx_index):
        tx = TronTransaction()
        tx.tx_id = tx_info.id_
        tx.tx_index = tx_index
        tx.block_id = blk.block_id
        tx.block_number = tx_info.block_number
        tx.block_timestamp = tx_info.block_timestamp
        tx.fee = tx_info.fee
        tx.contract_result = tx_info.contract_result
        tx.contract_address = tx_info.contract_address
        # tx.receipt = tx_info.receipt
        # receipt
        tx.result = True if tx_info.result is None else False
        tx.result_msg = "" if tx_info.result_msg is None else hex_to_words(tx_info.result_msg)
        tx.receipt_result = tx_info.receipt.get('result')
        tx.net_usage = tx_info.receipt.get('net_usage')
        tx.net_fee = tx_info.receipt.get('net_fee')
        tx.energy_fee = tx_info.receipt.get('energy_fee')
        tx.energy_usage_total = tx_info.receipt.get('energy_usage_total')
        tx.energy_penalty_total = tx_info.receipt.get('energy_penalty_total')
        # logs
        tx.logs = [] if tx_info.log == None else tx_info.log
        tx.internal_transactions = [] if tx_info.internal_transactions else tx_info.internal_transactions

        tx.ret = blk_tx.ret
        tx.signature = blk_tx.signature
        
        # raw_data 
        tx.contract = blk_tx.raw_data.get('contract')
        tx.ref_block_bytes = blk_tx.raw_data.get('ref_block_bytes')
        tx.ref_block_hash = blk_tx.raw_data.get('ref_block_hash')
        tx.expiration = blk_tx.raw_data.get('expiration')
        tx.timestamp = blk_tx.raw_data.get('timestamp')
        tx.fee_limit = blk_tx.raw_data.get('fee_limit')
        tx.raw_data_hex = blk_tx.raw_data_hex
        return tx
    

