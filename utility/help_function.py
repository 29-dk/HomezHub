import json

jsontype = "application/json"


def getrequest(request):

    if request.content_type == jsontype:
        data = json.loads(request.body)
    else:
        data = request.POST
    return data