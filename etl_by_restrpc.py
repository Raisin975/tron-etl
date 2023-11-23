from tronetl.restrpc.export_transactions_info import export_transactions_info
from tronetl.restrpc.export_blocks_and_transactions_by_getblockbynum import export_blocks_and_transactions_restrpc
from tronetl.restrpc.export_blocks_and_transactions import export_blocks_and_transactions
from tronetl.restrpc.extract_trc20_token_transfer import extract_trc20_token_transfers
from tronetl.restrpc.extract_trc10_token_transfer import extract_trc10_token_transfers
from tronetl.restrpc.export_contract import export_contracts


start_block = 34362000
end_block = 34370000
step = 1000
batch_size = 50
rpc_url = "http://127.0.0.1:8090"
max_worker = 10
data_save_path = "./data/rest"

# for start in range(start_block, end_block, step):
#     # [) 左闭右开
#     export_transactions_info(
#         start, min(start+step, end_block), batch_size, 
#         rpc_url,
#         max_worker, 
#         data_save_path + f"/transactions_info/{start}-{start+step}.json"
#     )

# for start in range(start_block, end_block, step):
#     # [) 左闭右开
#     export_blocks_and_transactions_restrpc(
#         start, min(start+step, end_block), batch_size, 
#         rpc_url,
#         max_worker, 
#         data_save_path + f"/blocks/{start}-{start+step}.json",
#         data_save_path + f"/transactions/{start}-{start+step}.json",
#     )

# # transaction and block
# for start in range(start_block, end_block, step):
#     export_blocks_and_transactions(
#         start, min(start+step, end_block), 
#         rpc_url=rpc_url,
#         batch_size=batch_size, 
#         max_workers=max_worker, 
#         transactions_output=data_save_path + f"/transactions/{start}-{start+step}.json",
#         block_output=data_save_path + f"/blocks/{start}-{start+step}.json"
#     )

# # trc20
# for start in range(start_block, end_block, step):
#     extract_trc20_token_transfers(
#         transactions=data_save_path + f"/transactions/{start}-{start+step}.json",
#         batch_size=batch_size, 
#         max_workers=max_worker, 
#         output=data_save_path + f"/trc20_transfers/{start}-{start+step}.json"
#     )

# trc10
for start in range(start_block, end_block, step):
    extract_trc10_token_transfers(
        transactions=data_save_path + f"/transactions/{start}-{start+step}.json",
        batch_size=batch_size, 
        rpc_url=rpc_url,
        max_workers=max_worker, 
        output=data_save_path + f"/trc10_transfers/{start}-{start+step}.json"
    )

# # contract
# for start in range(start_block, end_block, step):
#     export_contracts(
#         transactions=data_save_path + f"/transactions/{start}-{start+step}.json",
#         rpc_url=rpc_url,
#         batch_size=batch_size, 
#         max_workers=max_worker, 
#         output=data_save_path + f"/contracts/{start}-{start+step}.json"
#     )