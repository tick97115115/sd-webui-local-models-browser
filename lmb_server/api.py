from fastapi import FastAPI
from sqlmodel import Field, SQLModel, create_engine

def api_setup_hook(app: FastAPI):
    print('I\'ve been hooked!')
    return
