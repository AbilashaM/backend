import json
from json.decoder import JSONDecodeError
from pydantic import BaseModel, create_model
from typing import List

#function to convert as list
def tolist(rowstr):
    rowlist = []
    rowstr = json.loads(rowstr)
    for item in rowstr:
        rowlist.append(item)
    return rowlist

#function to convert as dictionary
def todict(rowstr):
    try:
        rowdict = json.loads(rowstr)
    except JSONDecodeError:
            rowdict = {}
    return rowdict

