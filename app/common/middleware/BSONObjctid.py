from bson import ObjectId


def BSONObjctid(objectid):
    response = ObjectId.is_valid(objectid)
    return response
