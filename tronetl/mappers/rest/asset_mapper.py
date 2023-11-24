from tronetl.domain.rest.asset import Asset
from tronetl.common.utils import hex_to_words


class TronAssetMapper(object):
    
    def json_dict_to_asset(self, json_dict):
        asset = Asset()
        asset.asset_name = hex_to_words(json_dict.get('name'))
        asset.token_id = json_dict.get('id')
        asset.owner_address = json_dict.get('owner_address')
        asset.abbr = hex_to_words(json_dict.get('abbr'))
        asset.total_supply = json_dict.get('total_supply')
        asset.trx_num = json_dict.get('trx_num')
        asset.num = json_dict.get('num')
        asset.start_time = json_dict.get('start_time')
        asset.end_time = json_dict.get('end_time')
        asset.description = hex_to_words(json_dict.get('description'))
        asset.url = hex_to_words(json_dict.get('url'))
        return asset

    def asset_to_dict(self, asset):
        return {
            'type': 'asset',
            'asset_name': asset.asset_name,
            'token_id': asset.token_id,
            'owner_address': asset.owner_address,
            'abbr': asset.abbr,
            'total_supply': asset.total_supply,
            'trx_num': asset.trx_num,
            'num': asset.num,
            'start_time': asset.start_time,
            'end_time': asset.end_time,
            'description': asset.description,
            'url': asset.url
        }