#!/usr/bin/env bash

set -e

export TESTING=True
export PROJECT_NAME=oscarine-api
export BACKEND_CORS_ORIGINS=http://localhost:8000
export SECRET_KEY=my-secret-key-for-testing

sudo docker run -d -e POSTGRES_USER=test -e POSTGRES_HOST_AUTH_METHOD=trust \
	--mount type=tmpfs,destination=/var/lib/postgresql/data \
	--rm -p 5433:5432 --name oscarine-test-db postgis/postgis:12-3.1-alpine

export TEST_DATABASE_URL="postgresql://test@localhost:5433/test"

# Sleep for 10 secs as database setup takes some time
echo "Waiting for database..."
sleep 6

echo "Checking db"
python app/tests_pre_start.py

echo "Creating btree_gist postgres extension"
sudo docker exec -it oscarine-test-db psql -U test -c "CREATE EXTENSION btree_gist;"

echo "Applying migrations..."
alembic upgrade head

bash ./scripts/test.sh "$@"

echo "Stopping database container"
sudo docker container stop oscarine-test-db

echo "I am done testing!"
unset TESTING
unset PROJECT_NAME
unset BACKEND_CORS_ORIGINS
unset SECRET_KEY
unset TEST_DATABASE_URL
