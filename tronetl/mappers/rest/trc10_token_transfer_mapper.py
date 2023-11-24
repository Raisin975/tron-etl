class Trc10TokenTransferMapper(object):
    
    def token_transfer_to_dict(self, token_transfer):
        return {
            'type': 'trc10_token_transfer',
            'asset_name': token_transfer.asset_name,
            'token_id': token_transfer.token_id,
            'owner_address': token_transfer.owner_address,
            'to_address': token_transfer.to_address,
            'amount': token_transfer.amount,
            'tx_id': token_transfer.tx_id,
            'block_number': token_transfer.block_number,
            'result': token_transfer.result,
            'result_msg': token_transfer.result_msg,
        }
