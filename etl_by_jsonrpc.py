from tronetl.jsonrpc.export_transactions import export_blocks_and_transactions


start_block = 47411590
end_block = 47411600
step = 1000
batch_size = 50
rpc_url = "http://127.0.0.1:50545/jsonrpc"
max_worker = 48
data_save_path = "./data"

for start in range(start_block, end_block, step):
    # [) 左闭右开
    export_blocks_and_transactions(
        start, start+step, batch_size, 
        rpc_url,
        max_worker, 
        blocks_output=data_save_path + f"/blocks/json/{start}-{start+step}.json",
        transactions_output=data_save_path + f"/transactions/json/{start}-{start+step}.json"
    )
