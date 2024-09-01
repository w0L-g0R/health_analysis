import dramatiq
from dependency_injector.containers import inject


class EventHandler:
    def __init__(
        self, subscription, encoder, repository, mapper
    ):
        self.subscription = subscription
        self.encoder = encoder
        self.mapper = mapper
        self.repository = repository

    @inject
    @dramatiq.actor
    def handle(self):
        for event in self.subscription:
            # encoder.encode(event)
            # event_data = validator.validate(event)
            # mapper.map(event_data)

            pass
