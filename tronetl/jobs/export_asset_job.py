from tronetl.executors.batch_work_executor import BatchWorkExecutor
from blockchainetl.jobs.base_job import BaseJob
from tronetl.mappers.rest.asset_mapper import TronAssetMapper
from tronetl.common.rest_rpc_requests import generate_asset_rest_rpc


class ExportAsset(BaseJob):
    def __init__(
            self,
            assets_iterable,
            batch_size, 
            max_workers,
            asset_provider,
            item_exporter
        ):
        self.assets_iterable = assets_iterable

        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self.asset_provider = asset_provider
        self.item_exporter = item_exporter

        self.asset_mapper = TronAssetMapper()

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(
            self.assets_iterable, 
            self._extract_assets
        )

    def _extract_assets(self, assets_list):
        assets_json_info = self.asset_provider.make_batch_request(list(generate_asset_rest_rpc(assets_list)))

        assets = [self.asset_mapper.json_dict_to_asset(asset_json) for asset_json in assets_json_info]
        
        for asset in assets:
            self.item_exporter.export_item(self.asset_mapper.asset_to_dict(asset))

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
