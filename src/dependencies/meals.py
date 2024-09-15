from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import (
    Dependency,
    Singleton,
)
from psycopg2.pool import SimpleConnectionPool

from api.meals.repository import MealsRepository


class Meals(DeclarativeContainer):
    pool = Dependency(instance_of=SimpleConnectionPool)

    repository = Singleton(MealsRepository, pool=pool)
