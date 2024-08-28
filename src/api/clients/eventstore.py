from esdbclient import EventStoreDBClient

from config import EVENTSTORE

# class EventStoreDbClient(EventStoreDBClient):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)


meals_subscription = EventStoreDBClient(
    uri=EVENTSTORE
).subscribe_to_stream(
    stream_name="stream_one",
    from_end=True,
)
