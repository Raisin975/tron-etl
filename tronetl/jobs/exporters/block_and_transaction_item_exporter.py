# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from blockchainetl.jobs.exporters.composite_item_exporter import CompositeItemExporter


RESTRPC_TRANSACTIONINFO_FIELDS_TO_EXPORT = [
    'id',
    'blockNumber',
    'blockTimeStamp',
    'contract_address',
    'contractResult',
    'fee',
    'receipt',
    'log',
    'internal_transactions',
    'result',
    'result_msg'
]

RESTRPC_TRANSACTION_FIELDS_TO_EXPORT = [
    'ret',
    'signature',
    'txID',
    'raw_data',
    'raw_data_hex',
]

RESTRPC_BLOCK_FIELDS_TO_EXPORT = [
    'blockID',
    'blockNumber',
    'txTrieRoot',
    'witnessAddress',
    'parentHash',
    'timestamp',
    'witnessSignature',
    'transactionCount'
]

JSONRPC_BLOCK_FIELDS_TO_EXPORT = [
    'number',
    'hash',
    'parent_hash',
    'nonce',
    'sha3_uncles',
    'logs_bloom',
    'transactions_root',
    'state_root',
    'receipts_root',
    'miner',
    'difficulty',
    'total_difficulty',
    'size',
    'extra_data',
    'gas_limit',
    'gas_used',
    'timestamp',
    'transaction_count',
    'base_fee_per_gas',
    'withdrawals_root',
    'withdrawals'
]

JSONRPC_TRANSACTION_FIELDS_TO_EXPORT = [
    'hash',
    'nonce',
    'block_hash',
    'block_number',
    'transaction_index',
    'from_address',
    'to_address',
    'value',
    'gas',
    'gas_price',
    'input',
    'block_timestamp',
    'max_fee_per_gas',
    'max_priority_fee_per_gas',
    'transaction_type'
]

def blocks_and_transactions_item_exporter_by_restrpc(blocks_output=None, transaction_output=None):
    return CompositeItemExporter(
        filename_mapping={
            'block': blocks_output,
            'block_transaction': transaction_output
        },
        field_mapping={
            'block': RESTRPC_BLOCK_FIELDS_TO_EXPORT, 
            'block_transaction': RESTRPC_TRANSACTION_FIELDS_TO_EXPORT
        }
    )

def transactions_info_item_exporter_by_restrpc(transactions_output=None):
    return CompositeItemExporter(
        filename_mapping={
            'transaction_info': transactions_output
        },
        field_mapping={
            'transaction_info': RESTRPC_TRANSACTIONINFO_FIELDS_TO_EXPORT
        }
    )

def blocks_and_transactions_item_exporter_by_jsonrpc(blocks_output=None, transactions_output=None):
    return CompositeItemExporter(
        filename_mapping={
            'block': blocks_output,
            'transaction': transactions_output
        },
        field_mapping={
            'block': JSONRPC_BLOCK_FIELDS_TO_EXPORT,
            'transaction': JSONRPC_TRANSACTION_FIELDS_TO_EXPORT
        }
    )