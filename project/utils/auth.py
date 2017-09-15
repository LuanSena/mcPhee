import os
import ast

from sanic.response import json

TOKENS = ast.literal_eval(os.environ.get('TOKENS', '{"1": "OFFLINE"}'))


def validate_auth_token(request, tokens=TOKENS):
    request_token = request.token
    company = None
    if request_token in tokens:
        company = tokens[request_token]
        is_authorized = True
    else:
        is_authorized = False

    if is_authorized:
        request["company"] = company
        return None
    else:
        return json({'status': 'not_authorized'}, 401)
