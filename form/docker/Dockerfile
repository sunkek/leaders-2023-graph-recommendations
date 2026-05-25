FROM node:20-alpine as builder
WORKDIR /usr/src/app
COPY ./app/package*.json ./
RUN npm install && npm cache clean --force
COPY ./app/ ./
RUN npm run build

FROM node:20-alpine as server
WORKDIR /usr/src/app
COPY --from=builder /usr/src/app/build ./build
RUN npm install --global http-server && adduser -D nonroot
USER nonroot
CMD ["http-server", "--port", "80", "-P", "http://0.0.0.0:80?", "/usr/src/app/build"]
