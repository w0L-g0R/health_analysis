# redis_broker = RedisBroker()
# dramatiq.set_broker(redis_broker)


class MealInsertEventHandler:
    def __init__(self, config, broker, queue_name):
        self.queue_name = queue_name
        self.actor = broker.actor(
            self.handle_insert_event,
            queue_name=self.queue_name,
        )

    async def handle(self, event):
        # Encode
        # Validate
        # Map event data to SQL args
        # Pipeline
        ##  Insert via Repo
        ##  Send Notification via Kafka to Notification Service
        print(f"Handling event in queue: {self.queue_name}")
        return
