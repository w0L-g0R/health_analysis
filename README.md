* RUN WORKERS FROM ROOT
dramatiq main 

* RUN DATASTORE FROM ROOT
poetry run python src/main.py


* SEND EVENTS FROM ROOT
poetry run python tests/events.py