from fastapi import FastAPI
from lmb_server.data_models import ResponseBody_Lora, Response_Loras
from lmb_server.api import api_setup_hook

def dev_entry(app: FastAPI):
    @app.get("/local-models-browser/api/v1/loras", response_model=Response_Loras)
    async def loras():
        # res = [extract_lora_info(obj) for obj in networks.available_networks.keys()]
        return Response_Loras(Loras=[], number=[].__len__())

    @app.get("/local-models-browser/api/v1/loras/{name}", response_model=ResponseBody_Lora)
    async def lora(name: str):
        return ResponseBody_Lora()
    
    api_setup_hook(app=app)

if __name__ == "__main__":
    app = FastAPI()
    dev_entry(app)
