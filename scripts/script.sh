# create a script to run the app
#!/bin/bash

# run the app
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000