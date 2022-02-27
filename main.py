from fastapi import FastAPI
import requests
import parser

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

session = requests.Session()
parser.start_parse(session)
