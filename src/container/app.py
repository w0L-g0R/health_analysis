from dependency_injector import providers
from dependency_injector.containers import (
    DeclarativeContainer,
)

from container.core import Core
from container.pools import Pools


class AppContainer(DeclarativeContainer):
    core = providers.Container(Core)
    config = core.config
    print("config app: ", config)

    pools = providers.Container(Pools, config=config)

    pass
