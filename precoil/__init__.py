# from config import coiled_config, CoiledConfig

from prefect.blocks.core import Block
from pydantic import SecretStr
import os
import dask


class CoiledConfig(Block):
    """A helper for running Coiled functions as tasks"""
    _block_type_name = "Precoil"
    _block_type_slug = "precoil"

    coiled_account: str
    coiled_token: SecretStr

    def configure(self):
        dask.config.set(
          {"coiled.token": self.coiled_token.get_secret_value(), 
          "coiled.account": self.coiled_account}
        )