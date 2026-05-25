import json

from app.service.database import db
from app.service.importer.model_city import CityNested
from app.service.importer.model_event import EventNested
from app.service.importer.model_excursion import ExcursionNested
from app.service.importer.model_hotel import HotelNested
from app.service.importer.model_place import PlaceNested
from app.service.importer.model_region import RegionNested
from app.service.importer.model_restaurant import RestaurantNested
from app.service.importer.model_route import RouteNested
from app.service.importer.model_tour import TourNested
from app.service.importer.model_track import TrackNested


path = "/usr/src/app/ds/"
import_data = (
    (RegionNested, "regions.json", db.upsert_region),
    (CityNested, "cities.json", db.upsert_city),
    (PlaceNested, "places.json", db.upsert_place),
    (HotelNested, "hotels.json", db.upsert_hotel),
    (RestaurantNested, "restaurants.json", db.upsert_restaurant),
    (EventNested, "events.json", db.upsert_event),
    (ExcursionNested, "excursions.json", db.upsert_excursion),
    (RouteNested, "routes.json", db.upsert_route),
    (TourNested, "tours.json", db.upsert_tour),
    (TrackNested, "tracks.json", db.upsert_track),
)


def import_all():  # TODO Использовать внешний маунт, не засорять контейнер данными
    print("Import started")
    for model, filename, func in import_data:
        with open(f"{path}{filename}") as f:
            data = json.load(f)
        for entry in data:
            func(model(**entry).get_flat_model())
        print(f"Imported {filename}")
        index = f"{filename[:-6]}_id"
        label = filename[:-6].capitalize()
        db.create_id_index(index=index, label=label)
        print(f"Created index for {label}")
    print("Import finished")
