import random

from dramatiq.brokers.rabbitmq import RabbitmqBroker

import testi
from testi2 import (
    DependencyInjectionMiddleware,
    NAppContainer,
)

napp = NAppContainer()

broker = RabbitmqBroker(
    url="amqp://guest:guest@127.0.0.1:5672",
    middleware=[DependencyInjectionMiddleware()],
)
# dramatiq.set_broker(broker)


def main():
    napp.init_resources()
    napp.wire(modules=[__name__, testi])
    napp.check_dependencies()

    # process.send(event_data=f"EVENT: {random.randint(1,100)}")


if __name__ == "__main__":
    main()
    testi.process.send(
        event_data=f"EVENT: {random.randint(1,100)}"
    )


# app = NAppContainer()
# app.init_resources()
# print("app: ", app)
# app.wire(modules=[__name__])

# dramatiq.set_broker(app.broker())


# app.check_dependencies()

# i = id(res)
# print("i: ", i)


# app = AppContainer()
# app.init_resources()
# app.wire(modules=[__name__])
# app.check_dependencies()

# process.send(event_data=f"EVENT: {random.randint(1,100)}")
