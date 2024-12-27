from fastapi import FastAPI
from lib.api import api_setup_hook

def main(app: FastAPI):
    api_setup_hook(app)
    return


