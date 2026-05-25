from datetime import datetime

from neo4j import GraphDatabase
from neo4j.graph import Node
from pydantic.main import BaseModel

from app.core.common import ObjectIdStr
from app.resource.activity.model import Activity, OfferType
from app.service.importer.model_city import City
from app.service.importer.model_event import Event
from app.service.importer.model_excursion import Excursion
from app.service.importer.model_hotel import Hotel
from app.service.importer.model_place import Place
from app.service.importer.model_region import Region
from app.resource.questionnaire.model import Questionnaire
from app.service.database.convert import node_to_dict
from app.service.database import queries as q
from app.service.importer.model_restaurant import Restaurant
from app.service.importer.model_tour import Tour
from app.service.importer.model_track import Track


import_dictionaries = {
    "5a673061e97c730010ac6281": Event,
    "5bb51b424390424300d06a41": Hotel,
    "626bc497e90ec71e9e3798d8": Restaurant,
}


class DB:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    @staticmethod
    def _get_questionnaire(tx, email: str) -> dict:
        result = tx.run(
            "MATCH (q:Questionnaire {email: $email}) "
            "RETURN q "
            "ORDER BY q.updated_at DESC "
            "LIMIT 1 ",
            email=email
        )
        result = result.single()
        if result is None:
            return {}
        node: Node = result[0]
        return node_to_dict(node)

    def get_questionnaire(self, email: str) -> dict:
        with self.driver.session() as session:
            return session.execute_read(self._get_questionnaire, email)

    def _upsert(self, obj: BaseModel, query: str) -> dict:
        obj.updated_at = datetime.now()
        data = obj.dict(exclude_none=True)
        # TODO Не загружать в ноду свойства, которые отражены связями
        properties = ", ".join(f"node.{k} = ${k}" for k in data)
        with self.driver.session() as session:
            result = session.run(query.format(properties=properties), data)
            result = result.single()

        if result is None:
            return {}
        return node_to_dict(result[0])

    def upsert_questionnaire(self, obj: Questionnaire) -> dict:
        return self._upsert(obj, q.UPSERT_QUESTIONNAIRE)

    def upsert_activity(self, obj: Activity) -> dict:
        data = {
            "email": obj.user_email,
            "offer_id": obj.offer_id,
            "updated_at": datetime.now(),
        }

        with self.driver.session() as session:
            result = session.run(q.UPSERT_ACTIVITY.format(
                offer_type=obj.offer_type.value.capitalize(), relationship=obj.type.upper()
            ), data)
            result = result.single()

        if result is None:
            return {}
        return node_to_dict(result[0])

    def upsert_region(self, obj: Region) -> dict:
        return self._upsert(obj, q.UPSERT_REGION)

    def upsert_city(self, obj: City) -> dict:
        return self._upsert(obj, q.UPSERT_CITY)

    def upsert_place(self, obj: Place) -> dict:
        return self._upsert(obj, q.UPSERT_PLACE)

    def upsert_hotel(self, obj: Hotel) -> dict:
        return self._upsert(obj, q.UPSERT_HOTEL)

    def upsert_restaurant(self, obj: Restaurant) -> dict:
        return self._upsert(obj, q.UPSERT_RESTAURANT)

    def upsert_event(self, obj: Event) -> dict:
        return self._upsert(obj, q.UPSERT_EVENT)

    def upsert_excursion(self, obj: Excursion) -> dict:
        return self._upsert(obj, q.UPSERT_EXCURSION)

    def upsert_route(self, obj: Excursion) -> dict:
        return self._upsert(obj, q.UPSERT_ROUTE)

    def upsert_tour(self, obj: Tour) -> dict:
        return self._upsert(obj, q.UPSERT_TOUR)

    def upsert_track(self, obj: Track) -> dict:
        return self._upsert(obj, q.UPSERT_TRACK)

    def create_id_index(self, index: str, label: str):
        with self.driver.session() as session:
            session.run(q.CREATE_ID_INDEX.format(index=index, label=label))

    def get_user_based_recommendations(
        self, email: str, object_type: OfferType, limit: int = 10
    ) -> list[dict[str, dict]]:
        with self.driver.session() as session:
            result = session.run(
                q.GET_USER_BASED_RECOMMENDATIONS.format(item_label=object_type.value.capitalize()),
                {"email": email, "limit": limit}
            )
            result = result.data()
        return result or []

    def get_item_based_recommendations(
        self, email: str, object_id: ObjectIdStr, object_type: OfferType, limit: int = 10
    ) -> list[dict[str, dict]]:
        with self.driver.session() as session:
            result = session.run(
                q.GET_ITEM_BASED_RECOMMENDATIONS.format(item_label=object_type.value.capitalize()),
                {"email": email, "id": object_id, "limit": limit}
            )
            result = result.data()
        return result or []

    def get_similar_recommendations(
        self, email: str, object_id: ObjectIdStr, object_type: OfferType, limit: int = 10
    ) -> list[dict[str, dict]]:
        with self.driver.session() as session:
            result = session.run(
                q.GET_SIMILAR_RECOMMENDATIONS.format(item_label=object_type.value.capitalize()),
                {"email": email, "id": object_id, "limit": limit}
            )
            result = result.data()
        return result or []

    def get_popular_recommendations(
            self, email: str, object_type: OfferType, limit: int = 10
    ) -> list[dict[str, dict]]:
        with self.driver.session() as session:
            result = session.run(
                q.GET_POPULAR_RECOMMENDATIONS.format(item_label=object_type.value.capitalize()),
                {"email": email, "limit": limit}
            )
            result = result.data()
        return result or []
