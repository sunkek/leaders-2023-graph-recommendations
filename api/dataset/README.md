# Sample dataset

These JSON files are **synthesized examples**, not real data. They mirror the
exact shape the importer consumes (see `api/app/service/importer/model_*.py`)
so the service runs end-to-end out of the box.

The original portal data from russpass.ru is third-party and not redistributed
here. Drop real exports in place of these files (same filenames) to run against
production data; the raw dump is gitignored (`/dataset/*.json`).

Entities are cross-linked by `ObjectId`:

```
region ── city ── place ─┬─ event
                         ├─ excursion / route / tour / track (route items)
                         ├─ hotel
                         └─ restaurant
```

Field reference per collection: `dataset/*_description.txt`.
