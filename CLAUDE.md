# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Travel recommendation microservice for the russpass.ru portal (Leaders 2023 hackathon). A Neo4j graph stores travel offers and user activity; a FastAPI backend serves graph-based recommendations; two React SPAs collect user questionnaires and trip requests.

## Architecture

Four containerized services behind a Traefik reverse proxy (TLS via Let's Encrypt). Domains and routing live in `docker-compose.yml` labels.

- **api/** — FastAPI backend (Python 3.11, Poetry, neo4j driver). The recommendation engine.
- **form/** — React SPA: new-user questionnaire (`form.recommender.suncake.xyz`).
- **form-recommend/** — React SPA: trip request form (`recommender.suncake.xyz`). Uses MUI + extra inputs vs `form/`.
- **neo4j** — graph DB (`neo4j:5.7.0`), ports 7474 (browser UI) / 7687 (bolt).
- Frontends are injected into the live russpass site via a browser JS injector (no server-side access to the site).

### API internals (`api/app/`)

- `main.py` — entrypoint. If `NEEDS_IMPORT=true`, runs `import_all()` before serving, then starts uvicorn via `service/rest/api.py`.
- `service/rest/router/` — three routers, all mounted in `api.py`:
  - `recommendation.py` — 4 GET strategies: `user_based`, `item_based`, `similar`, `popular`. All return `list[ObjectIdStr]`.
  - `questionnaire.py` — GET/POST user questionnaire data (keyed by email).
  - `activity.py` — POST user activity (view/favorite/order).
- `service/database/` — Neo4j access layer:
  - `client.py` — `DB` class wrapping the driver; `db` singleton. All queries run here.
  - `queries.py` — raw Cypher query strings. Recommendation queries (`GET_*_RECOMMENDATIONS`) use `.format(item_label=...)` to inject the node label; they exclude offers the user already favorited.
  - `convert.py` — `node_to_dict` for Neo4j nodes.
- `service/importer/` — loads `dataset/*.json` into the graph. `service.py` defines the `import_data` tuple (model, filename, upsert fn) and creates id indexes per label.
- `resource/` — domain models grouped by `model.py` (pydantic domain) + `schema.py` (request/response). `OfferType` enum (`activity/model.py`) is the canonical list of offer node labels: event, excursion, hotel, place, restaurant, route, tour, track.
- `core/config.py` — pydantic `BaseSettings`, loaded from env (`.env` / `api.env`). Key vars: `NEEDS_IMPORT`, `NEO4J_*`, `ENVIRONMENT`.
- `core/common.py` — `ObjectIdStr` (validates Mongo ObjectId strings, used as offer IDs throughout) and `Environment` enum.

### Conventions

- Offer IDs are Mongo `ObjectId` strings (`ObjectIdStr`), not Neo4j internal IDs — match graph nodes on the `id` property.
- User identity is currently the **email** field, not an auth token (see the recurring `# TODO Использовать access token` comments). Do not assume real auth exists.
- pydantic v1 API (`BaseSettings`, `.dict()`), matching FastAPI 0.95 — do not migrate to v2 idioms.
- Comments and docstrings are in Russian; keep that style when editing.

## Commands

Local dev (exposes api:8000, form:8080, form-recommend:8081, neo4j:7474/7687):
```sh
docker compose -f docker-compose.dev.yml up --build
```

Frontend (run inside `form/app` or `form-recommend/app`):
```sh
npm install
npm start          # dev server
npm run build      # production build
npm test           # react-scripts test (Jest)
```

API dependency regen (after adding Python libs):
```sh
cd api && poetry export -f requirements.txt --output requirements.txt
```

Load testing (Locust, UI at http://0.0.0.0:8089):
```sh
cd load-test && docker compose up
```

Production deploy: build + push images to `registry.gitlab.com/sunkek/leaders2023:{api,form,form-recommend,traefik}`, then `docker compose pull && docker compose up -d` on the server. See `readme.md` for full steps.

## Notes

- The API Docker image bakes `dataset/` into the image (`COPY ./dataset ./ds`); import reads from `/usr/src/app/ds/`.
- There is no Python test suite in `api/`.
- Live swagger: https://api.recommender.suncake.xyz/docs
