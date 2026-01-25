#!/bin/sh

# Run migrations before starting the app
echo "Running database migrations..."
if alembic upgrade head; then
    echo "Migrations completed successfully"
else
    echo "Warning: Migrations failed, but continuing to start the app..."
    echo "You may need to run migrations manually: alembic upgrade head"
fi

# Run the app
echo "Starting application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000