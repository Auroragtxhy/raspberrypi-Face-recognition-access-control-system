import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


def httpFunc(url, person, time, result, path, pictureName):
    Headers = {"Accept": "*/*"}
    data = MultipartEncoder(
        fields={
            'person': person,
            'time': time,
            'result': result,
            "photoFiles": (pictureName, open(path, 'rb'), "image/jpg")
        }
    )
    print(data.content_type)
    Headers["Content-Type"] = data.content_type
    print(Headers)
    r = requests.post(url=url, data=data, headers=Headers)
    return r
