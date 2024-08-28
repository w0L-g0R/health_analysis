import dramatiq
from dramatiq.brokers.rabbitmq import RabbitmqBroker

broker = RabbitmqBroker()
# broker.add_middleware(Results(backend=RedisBackend()))
dramatiq.set_broker(broker)
