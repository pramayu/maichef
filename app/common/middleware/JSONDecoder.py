from bson import ObjectId

def JSONDecoder(userid):
    objId = ObjectId(str(userid))
    return objId
