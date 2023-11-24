import json

from blockchainetl.file_utils import smart_open
from blockchainetl.jobs.exporters.converters.int_to_string_item_converter import IntToStringItemConverter
from tronetl.jobs.exporters.asset_item_exporter import asset_item_exporter
from tronetl.providers.auto import get_rest_provider_from_uri
from tronetl.common.thread_local_proxy import ThreadLocalProxy
from tronetl.jobs.export_asset_job import ExportAsset
from blockchainetl.logging_utils import logging_basic_config

logging_basic_config()

GET_ASSET = '/wallet/getassetissuebyid'

def export_assets(
    asseti_ids, rpc_url,
    batch_size, max_workers, 
    output, values_as_strings=False
):
    with smart_open(asseti_ids, 'r') as assets_file:
        if asseti_ids.endswith('.json'):
            assets_reader = (
                asset_id.strip() for asset_id in assets_file
                if asset_id.strip()
            )
        else:
            return 
        assets_reader = ['1003406', '1004992']   
        converters = [IntToStringItemConverter(keys=['value'])] if values_as_strings else []
        job = ExportAsset(
            assets_iterable=assets_reader,
            batch_size=batch_size,
            max_workers=max_workers,
            asset_provider=ThreadLocalProxy(lambda : get_rest_provider_from_uri(
                rpc_url + GET_ASSET,
                'POST'
            )),
            item_exporter=asset_item_exporter(output, converters=converters)
        )
        job.run()

