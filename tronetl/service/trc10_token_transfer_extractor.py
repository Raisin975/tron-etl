from tronetl.domain.rest.trc10_transfer import Trc10TokenTransfer
from tronetl.common.utils import hex_to_words

class Trc10TokenTransferExtractor(object):

    def extract_transfer_from_contract_and_tx(self, contract_parameter_value_and_tx):
        tx = contract_parameter_value_and_tx[0]
        contract_parameter_value = contract_parameter_value_and_tx[1]

        token_transfer = Trc10TokenTransfer()
        token_transfer.asset_name = None
        token_transfer.token_id = hex_to_words(contract_parameter_value.get('asset_name'))
        token_transfer.owner_address = contract_parameter_value.get('owner_address')
        token_transfer.to_address = contract_parameter_value.get('to_address')
        token_transfer.amount = contract_parameter_value.get('amount')
        
        token_transfer.tx_id = tx.tx_id
        token_transfer.block_number = tx.block_number
        token_transfer.result = tx.result
        token_transfer.result_msg = tx.result_msg
        return token_transfer

