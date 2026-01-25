# create a script to run the app
#!/bin/sh

# Run the app
echo "Starting application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000