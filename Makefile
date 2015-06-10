configure:
	pip install -r requirements.txt
server:
	python server.py
db:
	python lib/database_setup.py
fulldb:
	python lib/populate_db.py && python lib/populate_db.py

.PHONY: configure server db fulldb
