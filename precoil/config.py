from prefect.blocks.core import Block
from pydantic import SecretStr
import os


def coiled_config(func, blockname: str = None):

  def wrapper(*args, **kwargs):
    coilblock = CoiledConfig(blockname)
    
    os.environ['DASK_COILED__ACCOUNT'] = coilblock.coiled_account
    os.environ['DASK_COILED__TOKEN'] = coilblock.coiled_token.get_secret_value()

    result = func(*args, **kwargs)

    # Remove the example environment variable
    del os.environ['DASK_COILED__ACCOUNT']
    del os.environ['DASK_COILED__TOKEN']

    return result

  return wrapper


class CoiledConfig(Block):
    """A helper for running Coiled functions as tasks"""
    _block_type_name = "Precoil"
    _block_type_slug = "precoil"

    coiled_account: str
    coiled_token: SecretStr

