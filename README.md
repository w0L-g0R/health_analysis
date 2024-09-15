* RUN WORKERS FROM ROOT
dramatiq main 

* RUN DATASTORE FROM ROOT
poetry run python src/main.py


* SEND EVENTS FROM ROOT
poetry run python tests/events.py

* CONNECTING TO THE SERVICE IN pg_service.conf FROM ROOT
PGSERVICEFILE=pg_service.conf pgcli service=timescaledb
