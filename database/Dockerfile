FROM mongo:latest
ENV MONGO_INITDB_ROOT_USERNAME=root
ENV MONGO_INITDB_ROOT_PASSWORD=rootpasswd
ENV MONGO_INITDB_DATABASE=admin
COPY init-mongo.js /docker-entrypoint-initdb.d/init-mongo.js