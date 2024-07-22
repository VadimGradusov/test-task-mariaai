"""Save json instrument"""
import json
import os
import uuid


def save_json(**data):
    """Save json with passed arguments"""
    try:
        with open(f'{os.getcwd()}/src/resources/results/{uuid.uuid4()}.json', 'w') as file:
            file.write(str(data).replace("'", '"'))
    except KeyError as error:
        return f'Error: {error}'
    return 'Json saved'