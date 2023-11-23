from tronetl.domain.rest.log import Log
from tronetl.common.utils import to_normalized_address, to_41_address

class LogMapper(object):

    def json_dict_to_log(self, json_dict, transaction, log_index):
        log = Log()
        log.log_index = log_index
        log.address = to_41_address(to_normalized_address(json_dict.get('address')))
        log.data = json_dict.get('data')
        log.topics = json_dict.get('topics')
        log.block_id = transaction.block_id
        log.block_number = transaction.block_number
        log.tx_id = transaction.tx_id
        log.tx_index = transaction.tx_index
        return log
