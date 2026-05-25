from datetime import datetime

from neo4j.graph import Node
from neo4j.time import DateTime

def node_to_dict(node: Node) -> dict:
    res = {}
    for k, v in node.items():
        if isinstance(v, DateTime):
            res[k] = datetime(
                v.year, v.month, v.day,
                v.hour, v.minute, v.second,
                tzinfo=v.tzinfo,
            )
        else:
            res[k] = v
    return res
