from dramatiq.brokers.rabbitmq import RabbitmqBroker

broker = RabbitmqBroker(
    url="amqp://guest:guest@127.0.0.1:5672"
)
# broker.add_middleware(Results(backend=RedisBackend()))
