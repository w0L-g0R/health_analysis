import dramatiq
from dramatiq.brokers.redis import RedisBroker

from api.meals.domain.events.meals.insert import InsertMealEvent

# redis_broker = RedisBroker()
# dramatiq.set_broker(redis_broker)

class InsertMealEventHandler:
    
    def __init__(self, config, broker, queue_name):
        self.queue_name = queue_name
        self.actor = broker.actor(self.handle_insert_event, queue_name=self.queue_name)
        
    async def handle(self, event):
        # Encode
        # Validate
        # SQL Statement
        # SQL args
        print(f"Handling event in queue: {self.queue_name}")
        return