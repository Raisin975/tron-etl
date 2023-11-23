class TokenTransferMapper(object):
    
    def token_transfer_to_dict(self, token_transfer):
        return {
            'type': 'token_transfer',
            'token_address': token_transfer.token_address,
            'from_address': token_transfer.from_address,
            'to_address': token_transfer.to_address,
            'value': token_transfer.value,
            'tx_id': token_transfer.tx_id,
            'log_index': token_transfer.log_index,
            'block_number': token_transfer.block_number,
            'decimals': token_transfer.decimals
        }
