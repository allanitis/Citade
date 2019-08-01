from botocore.vendored import requests

def handler(event, context):
    
    return {"message": "Successfully executed"}
    try:
        res = requests.post(
            "http://bx8ocdir2g.execute-api.eu-west-1.amazonaws.com/prod/fyn",
            params={},
            headers={"Accept":"","Content-Type":"applications/json"},
            data=''
        )
        # your code goes here
    except BaseException as e:
        # error handling goes here
        raise(e)
