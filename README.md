# Coiled config block

Running coiled functions as tasks from Prefect flows is awesome. This little block simply contains and configures the credentials needed, so you can get started quickly.

## Before you begin

There is some config needed to set up coiled so that it can spin up cloud resources on your behalf. Check out the Coiled documentation for how to do that.

## Register block
Register a CoiledConfig block:

```py
from precoil import CoiledConfig

cc = CoiledConfig(
    coiled_account = "<my-coiled-account-name>",
    coiled_token = "<my-secret-token>"
)

cc.save('cc', overwrite=True)
```

## Example flow

Using the block to set up the config is really simple. Simply load the block and run the `configure()` method. This configures dask to use Coiled with the provided credentials.

```py
from prefect import task, flow
from precoil import CoiledConfig
from prefect import get_run_logger
import coiled

@task
def get_new_data_files():
    files = ["Hello", "World"]
    return files

@task
@coiled.function()
def process(file):
    results = file.upper()
    print(f"Processing {file}...")
    return results

@flow(name="Coiled")
def coiled():

    logger = get_run_logger()
    CoiledConfig.load('radcoiled').configure()

    files = get_new_data_files()
    futures = process.map(files)
    for future in futures:
        logger.info(f"Done with {future.result()}")

if __name__ == '__main__':
    coiled()
```

Running this file should execute the flow and spin up a coiled cluster to run the `process` task.