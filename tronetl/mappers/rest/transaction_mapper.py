from tronetl.domain.rest.transaction import TronBlockTransaction, TronTransactionInfo, TronTransaction


# /wallet/gettransactioninfobyid
class TronTransactionInfoMapper(object):
    
    def json_dict_to_transaction(self, json_dict):
        transaction = TronTransactionInfo()
        transaction.id_ = json_dict.get('id')
        transaction.block_number = json_dict.get('blockNumber')
        transaction.contract_address = json_dict.get('contract_address')
        transaction.contract_result = json_dict.get('contractResult')
        transaction.block_timestamp = json_dict.get('blockTimeStamp')
        transaction.fee = json_dict.get('fee')
        transaction.receipt = json_dict.get('receipt')
        transaction.log = json_dict.get('log')
        transaction.internal_transactions = json_dict.get('internal_transactions')
        transaction.result = json_dict.get('result')
        transaction.result_msg = json_dict.get('resMessage')
        return transaction

    def transaction_to_dict(self, transaction):
        return {
            'type': 'transaction_info',
            'id': transaction.id_,
            'blockNumber': transaction.block_number,
            'contract_address': transaction.contract_address,
            'contractResult': transaction.contract_result,
            'blockTimeStamp': transaction.block_timestamp,
            'fee': transaction.fee,
            'receipt': transaction.receipt,
            'log': transaction.log,
            'internal_transactions': transaction.internal_transactions,
        }


# /wallet/gettransactionbyid
class TronBlockTransactionMapper(object):
    def json_dict_to_transaction(self, json_dict):
        transaction = TronBlockTransaction()
        transaction.ret = json_dict.get('ret')
        transaction.signature = json_dict.get('signature')
        transaction.txID = json_dict.get('txID')
        transaction.raw_data = json_dict.get('raw_data')
        transaction.raw_data_hex = json_dict.get('raw_data_hex')
        return transaction

    def transaction_to_dict(self, transaction):
        return {
            'type': 'block_transaction',
            'ret': transaction.ret,
            'signature': transaction.signature,
            'txID': transaction.txID,
            'raw_data': transaction.raw_data,
            'raw_data_hex': transaction.raw_data_hex,
        }


class TronTransactionMapper(object):
    def json_dict_to_transaction(self, json_dict):
        tx = TronTransaction()
        tx.tx_id = json_dict.get('tx_id')
        tx.block_id = json_dict.get('block_id')
        tx.block_number = json_dict.get('block_number')
        tx.block_timestamp = json_dict.get('block_timestamp')
        tx.fee = json_dict.get('fee')
        tx.contract_result = json_dict.get('contract_result')
        tx.contract_address = json_dict.get('contract_address')
 
        tx.result = json_dict.get('result')
        tx.result_msg = json_dict.get('result_msg')
        tx.receipt_result = json_dict.get('receipt_result')
        tx.net_usage = json_dict.get('net_usage')
        tx.net_fee = json_dict.get('net_fee')
        tx.energy_fee = json_dict.get('energy_fee')
        tx.energy_usage_total = json_dict.get('energy_usage_total')
        tx.energy_penalty_total = json_dict.get('energy_penalty_total')

        tx.logs = [] if json_dict.get('logs') == None else json_dict.get('logs')
        tx.internal_transactions = [] if json_dict.get('internal_transactions') is None else json_dict.get('internal_transactions')

        tx.ret = json_dict.get('ret')
        tx.signature = json_dict.get('signature')

        tx.contract = [] if json_dict.get('contract') == None else json_dict.get('contract')
        tx.owner_address = json_dict.get('owner_address')
        tx.tx_type = json_dict.get('tx_type')
        tx.ref_block_bytes = json_dict.get('ref_block_bytes')
        tx.ref_block_hash = json_dict.get('ref_block_hash')
        tx.expiration = json_dict.get('expiration')
        tx.fee_limit = json_dict.get('fee_limit')
        tx.timestamp = json_dict.get('timestamp')
        tx.raw_data_hex = json_dict.get('raw_data_hex')
        return tx

    def transaction_to_dict(self, transaction):
        return {
            'type': 'transaction',
            'tx_id': transaction.tx_id,
            'tx_index': transaction.tx_index,
            'block_id': transaction.block_id,
            'block_number': transaction.block_number,
            'block_timestamp': transaction.block_timestamp,
            'fee': transaction.fee,
            'contract_result': transaction.contract_result,
            'receipt_result': transaction.receipt_result,
            'result_msg': transaction.result_msg,
            'result': transaction.result,
            'net_usage': transaction.net_usage,
            'net_fee': transaction.net_fee,
            'energy_fee': transaction.energy_fee,
            'energy_usage_total': transaction.energy_usage_total,
            'energy_penalty_total': transaction.energy_penalty_total,
            'contract_address': transaction.contract_address,
            'contract_address': transaction.contract_address,
            'logs': transaction.logs,
            'internal_transactions': transaction.internal_transactions,
            'ret': transaction.ret,
            'signature': transaction.signature,
            'contract': transaction.contract,
            'owner_address': transaction.owner_address,
            'tx_type': transaction.type,
            'ref_block_bytes': transaction.ref_block_bytes,
            'ref_block_hash': transaction.ref_block_hash,
            'expiration': transaction.expiration,
            'fee_limit': transaction.fee_limit,
            'timestamp': transaction.timestamp,
            'raw_data_hex': transaction.raw_data_hex,
        }
