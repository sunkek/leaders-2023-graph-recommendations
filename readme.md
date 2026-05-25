# Travel Recommendation Microservice

A graph-based recommendation engine for the [russpass.ru](https://russpass.ru/) travel portal, built for the **Leaders 2023** hackathon. The project reached the finals and placed **4th out of 10 finalist teams**.

## What it does

Given a user's questionnaire answers and their activity (views, favorites), the service recommends travel offers — events, excursions, hotels, places, restaurants, routes, tours, and tracks. Recommendations come from a Neo4j graph using four strategies:

- **User-based** — offers favored by users with similar profiles.
- **Item-based** — offers favored by users who engaged with the same item.
- **Similar** — offers structurally close in the graph (shared properties).
- **Popular** — most-engaged offers overall.

Each strategy excludes offers the user already favorited.

## Architecture

Four services run behind a [Traefik](https://traefik.io/) reverse proxy (TLS via Let's Encrypt):

| Service | Stack | Role |
| --- | --- | --- |
| `api` | FastAPI · Python 3.11 · Poetry | Recommendation engine and REST API |
| `form` | React SPA | New-user questionnaire (`form.recommender.suncake.xyz`) |
| `form-recommend` | React SPA · MUI | Trip request form (`recommender.suncake.xyz`) |
| `neo4j` | Neo4j 5.7 | Graph store for offers and user activity |

The graph is seeded from `dataset/*.json` on first boot (`NEEDS_IMPORT=true`). Offer IDs are Mongo `ObjectId` strings carried over from the source data.

Because we could not modify the russpass site directly, the frontends are injected into the live site client-side via a browser JS injector.

### API layout (`api/app/`)

- `service/rest/router/` — `recommendation`, `questionnaire`, `activity` routers.
- `service/database/` — Neo4j access layer (`client.py`) and raw Cypher (`queries.py`).
- `service/importer/` — loads the dataset into the graph and builds id indexes.
- `resource/` — pydantic domain models and request/response schemas.
- `core/config.py` — env-driven settings (`NEO4J_*`, `ENVIRONMENT`, `NEEDS_IMPORT`).

> User identity is currently the email field rather than a real access token — a known shortcut for the demo.

## Prerequisites

- A host with a recent Docker install.
- Open firewall ports: `80`, `443`, `7474`, `7687`.

Demo server specs: 4 vCPUs, 8 GiB RAM, 60 GB SSD, 50 Mbit/s.

## Local development

Brings up the API on `:8000`, the forms on `:8080` / `:8081`, and Neo4j on `:7474` / `:7687`:

```sh
docker compose -f docker-compose.dev.yml up --build
```

Run a frontend on its own (inside `form/app` or `form-recommend/app`):

```sh
npm install
npm start          # dev server
npm run build      # production build
npm test           # tests
```

Regenerate Python dependencies after adding a library:

```sh
cd ./api
poetry export -f requirements.txt --output requirements.txt
```

## Deployment

Build and push images to the container registry:

```sh
cd ./api             && docker build -t registry.gitlab.com/sunkek/leaders2023:api             -f ./docker/Dockerfile .
cd ./form            && docker build -t registry.gitlab.com/sunkek/leaders2023:form            -f ./docker/Dockerfile .
cd ./form-recommend  && docker build -t registry.gitlab.com/sunkek/leaders2023:form-recommend  -f ./docker/Dockerfile .

docker push registry.gitlab.com/sunkek/leaders2023:api
docker push registry.gitlab.com/sunkek/leaders2023:form
docker push registry.gitlab.com/sunkek/leaders2023:form-recommend
```

On the server, add the env files (per the `.env.example` templates) next to `docker-compose.yml`, then pull and start:

```sh
cd /root/recommender
docker compose pull
docker compose up -d
```

## Load testing

Uses [Locust](https://locust.io/):

```sh
cd ./load-test
docker compose up
```

Open the Locust UI at `http://0.0.0.0:8089` and set the desired load. Example: 120 peak users, spawn rate 10/s, host `https://api.recommender.suncake.xyz`.

## Links

- [Presentation](https://docs.google.com/presentation/d/1DGjjwBkqCRjuqKRaO8LNDOqqddGsDPi5)
- [Supporting documentation](https://docs.google.com/document/d/1wF343l1j2X8QDQAkafbE9cbMMmWraxxUHLAnY82VWN4)
- [Verification documentation](https://docs.google.com/document/d/1SSbmG64g6GxzmRtDg17nFARTZwkHAfVFQaRbj0rCfQg)
