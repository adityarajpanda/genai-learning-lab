# We need to create a FastAPI POST endpoint in which we will accept a list of course objects, validate them and 
# stores them into a JSON file.

import json
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

course = 