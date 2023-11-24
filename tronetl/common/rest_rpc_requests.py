def generate_transaction_rest_rpc(block_numbers):
    for block_number in block_numbers:
        yield (
            generate_block_num_rest_rpc(
                block_number
            ), 
            generate_block_num_rest_rpc(
                block_number
            )
        )

def generate_get_txinfo_by_blocknumber_rest_rpc(block_numbers):
    for block_number in block_numbers:
        yield generate_block_num_rest_rpc(
            block_number
        )

def generate_get_block_by_num_rest_rpc(block_numbers):
    for block_number in block_numbers:
        yield generate_block_num_rest_rpc(
            block_number
        )

def generate_block_num_rest_rpc(block_number):
    return {
        'num': block_number
    }

def generate_asset_rest_rpc(assets_id_list):
    for asset_id in assets_id_list:
        yield {
            'value': asset_id
        }

def generate_contract_rest_rpc(contract_addresses):
    for address in contract_addresses:
        yield {
            'value': address
        }
