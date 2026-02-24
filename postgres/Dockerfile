ARG POSTGRES_VERSION=18
FROM postgres:${POSTGRES_VERSION}

USER root

ARG OPTIONAL_POSTGIS
ARG POSTGRES_VERSION=18

RUN if [ "$OPTIONAL_POSTGIS" = "true" ] || [ "$OPTIONAL_POSTGIS" = "True" ]; then \
        apt-get update && \
        apt-get install -y ca-certificates gnupg curl lsb-release && \
        curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor | tee /etc/apt/trusted.gpg.d/apt.postgresql.org.gpg >/dev/null && \
        sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' && \
        apt-get update && \
        apt-get install -y postgresql-"$POSTGRES_VERSION"-postgis-3 postgis && \
        rm -rf /var/lib/apt/lists/* ; \
    fi

COPY postgres/init-postgis.sh /docker-entrypoint-initdb.d/