DC = docker compose
STORAGES_FILE = docker_compose/storages.yaml
EXEC = docker exec -it
DB_CONTAINER = postgres_db
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker_compose/app.yaml
APP_CONTAINER_1 = django1
APP_CONTAINER_2 = django2
MANAGE_PY = python manage.py
USER = -U postgres
MAKE_APP = ${DC} -f ${APP_FILE} -f ${STORAGES_FILE} ${ENV} up --build -d
MAKE_APP_DOWN = ${DC} -f ${APP_FILE} -f ${STORAGES_FILE} down
MAKE_APP_LOGS = ${LOGS} ${APP_CONTAINER_1} -f

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up -d

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down

.PHONY: postgres
postgres:
	${EXEC} ${DB_CONTAINER} psql ${USER}

.PHONY: storages-logs
storages-logs:
	${LOGS} ${DB_CONTAINER} -f

.PHONY: app
app:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} ${ENV} up --build -d

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER_1} -f

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} down

.PHONY: migrate
migrate:
	${EXEC} ${APP_CONTAINER_1} ${MANAGE_PY} migrate

.PHONY: migrations
migrations:
	${EXEC} ${APP_CONTAINER_1} ${MANAGE_PY} makemigrations

.PHONY: superuser
superuser:
	${EXEC} ${APP_CONTAINER_1} ${MANAGE_PY} createsuperuser

.PHONY: collectstatic
collectstatic:
	${EXEC} ${APP_CONTAINER_1} ${MANAGE_PY} collectstatic


.PHONY: app-relaod
app-reload:
	${MAKE_APP_DOWN} && ${MAKE_APP} && ${MAKE_APP_LOGS}