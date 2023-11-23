from tronetl.common.utils import chunk_string, hex_to_dec, to_normalized_address, to_41_address
from tronetl.domain.rest.trc20_transfer import Trc20TokenTransfer

import logging 

TRANSFER_EVENT_TOPIC = 'ddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
logger = logging.getLogger(__name__)


class Trc20TokenTransferExtractor(object):

    def extract_transfer_from_log(self, log, tx):
        topics = log.topics
        if topics is None or len(topics) < 1:
            # This is normal, topics can be empty for anonymous events
            return None

        if (topics[0]).casefold() == TRANSFER_EVENT_TOPIC:
            # Handle unindexed event fields
            topics_with_data = topics + split_to_words(log.data)
            # if the number of topics and fields in data part != 4, then it's a weird event
            if len(topics_with_data) != 4:
                logger.warning("The number of topics and data parts is not equal to 4 in log {} of transaction {}"
                               .format(log.log_index, log.tx_id))
                return None

            token_transfer = Trc20TokenTransfer()
            token_transfer.token_address = log.address
            token_transfer.from_address = word_to_address(topics_with_data[1])
            token_transfer.to_address = word_to_address(topics_with_data[2])
            token_transfer.value = hex_to_dec(topics_with_data[3])
            
            token_transfer.tx_id = log.tx_id
            token_transfer.log_index = log.log_index
            token_transfer.block_number = log.block_number
            
            token_transfer.result = tx.result
            token_transfer.result_msg = tx.result_msg

            return token_transfer

        return None



def split_to_words(data):
    if data and len(data) > 2:
        data_without_0x = data[2:]
        words = list(chunk_string(data_without_0x, 64))
        words_with_0x = list(map(lambda word: '0x' + word, words))
        return words_with_0x
    return []


def word_to_address(param):
    if param is None:
        return None
    elif len(param) >= 40:
        return to_41_address(to_normalized_address(param[-40:]))
    else:
        return to_41_address(to_normalized_address(param))
