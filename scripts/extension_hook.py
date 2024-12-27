import enum
import os
from modules import ui_extra_networks, script_callbacks, shared

import gradio as gr
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

import networks
import network

from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Dict, List, Union, Any
from dataclasses import dataclass

from modules.ui_extra_networks import quote_js

from lmb_server.data_models import TagFrequency, DatasetDirs, BucketInfo, Buckets, Metadata, UserMetadata, ResponseBody_Lora, ErrorResponse, Response_Loras

class ExtraNetworksPageCustom(ui_extra_networks.ExtraNetworksPage):
    def __init__(self):
        super().__init__('Local Models Browser')  # Set the tab name
        self.allow_negative_prompt = True  # Optional: Enable integration with negative prompts

    def create_item(self, name, index=None, enable_filter=True):
        return

    def list_items(self):
        return
    
    def create_html(self, tabname, *, empty=False):
        fastapi_endpoint = f'/local-models-browser/static/'
        return f'<iframe src="{fastapi_endpoint}" width="100%" height="500px" style="border:none;"></iframe>'

network_page = ExtraNetworksPageCustom()

# class Lora(BaseModel):
#     name: str
#     filename: str
#     metadata: dict[str, Any]
#     is_safetensors: bool
#     alias: str
#     hash: str
#     shorthash: str
#     sd_version: str
#     mtime: float
#     preview: str | None
#     description: str | None
#     search_terms: list[str]

# def load_network(network_on_disk):
#     path, ext = os.path.splitext(network_on_disk.filename)
#     search_terms = [network_page.search_terms_from_path(network_on_disk.filename)]
#     if network_on_disk.hash:
#         search_terms.append(network_on_disk.hash)
    
#     net = Lora(
#         name = network_on_disk.name,
#         filename = network_on_disk.filename,
#         metadata = network_on_disk.metadata,
#         is_safetensors = network_on_disk.is_safetensors,
#         alias = network_on_disk.alias,
#         hash = network_on_disk.hash,
#         shorthash = network_on_disk.shorthash,
#         sd_version = network.SdVersion(network_on_disk.sd_version).name,
#         mtime = os.path.getmtime(network_on_disk.filename),
#         preview = network_page.find_preview(path) or network_page.find_embedded_preview(path, network_on_disk.name, network_on_disk.metadata),
#         description = network_page.find_description(path),
#         search_terms = search_terms
#     )
    
#     return net



def before_ui():
    """Register your custom tab."""
    ui_extra_networks.register_page(network_page)

def extract_lora_info(name:str):
    lora_on_disk = networks.available_networks.get(name)
    if lora_on_disk is None:
        return
    path, ext = os.path.splitext(lora_on_disk.filename)
    alias = lora_on_disk.get_alias()
    search_terms = [network_page.search_terms_from_path(lora_on_disk.filename)]
    if lora_on_disk.hash:
        search_terms.append(lora_on_disk.hash)
    item = {
        "name": name,
        "filename": lora_on_disk.filename,
        "shorthash": lora_on_disk.shorthash,
        "preview": network_page.find_preview(path) or network_page.find_embedded_preview(path, name, lora_on_disk.metadata),
        "description": network_page.find_description(path),
        "search_terms": search_terms,
        "local_preview": f"{path}.{shared.opts.samples_format}",
        "metadata": lora_on_disk.metadata,
        # "sort_keys": {'default': index, **network_page.get_sort_keys(lora_on_disk.filename)},
    }
    network_page.read_user_metadata(item)
    activation_text = item["user_metadata"].get("activation text")
    preferred_weight = item["user_metadata"].get("preferred weight", 0.0)
    item["prompt"] = quote_js(f"<lora:{alias}:") + " + " + (str(preferred_weight) if preferred_weight else "opts.extra_networks_default_multiplier") + " + " + quote_js(">")
    if activation_text:
        item["prompt"] += " + " + quote_js(" " + activation_text)
    negative_prompt = item["user_metadata"].get("negative text", "")
    item["negative_prompt"] = quote_js(negative_prompt)
    #   filter displayed loras by UI setting
    sd_version = item["user_metadata"].get("sd version")
    if sd_version in network.SdVersion.__members__:
        item["sd_version"] = sd_version
        sd_version = network.SdVersion[sd_version]
    else:
        sd_version = lora_on_disk.sd_version        #   use heuristics
        #sd_version = network.SdVersion.Unknown     #   avoid heuristics 
    item["sd_version_str"] = str(sd_version)
    item["ctime"] = os.path.getctime(lora_on_disk.filename)
    return item


def api_networks(_: gr.Blocks, app: FastAPI):
    from os.path import join, dirname
    flutter_build_dir = join(dirname(dirname(__file__)), "ui", "build", "web")
    print(f"flutter_build_dir: {flutter_build_dir}")
    html_path = join(flutter_build_dir, "index.html")
    app.mount("/local-models-browser/static", StaticFiles(directory=flutter_build_dir, html=True), name="local-models-browser-static")
    
    @app.get("/local-models-browser/static")
    async def home():
        return FileResponse(html_path, media_type="text/html")
    
    @app.get("/local-models-browser/api/v1/loras", response_model=Response_Loras)
    async def loras():
        res = [extract_lora_info(obj) for obj in networks.available_networks.keys()]
        return Response_Loras(Loras=res, number=res.__len__())

    @app.get("/local-models-browser/api/v1/loras/{name}", response_model=ResponseBody_Lora)
    async def lora(name: str):
        return extract_lora_info(name)

    @app.exception_handler(Exception)
    async def validation_exception_handler(request, exc: ValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "detail": "Response model validation error",
                "errors": exc.errors(),
            },
        )
    
    @app.get("/local-models-browser/api/v1/loras/names/", response_model=List[str])
    async def lora_names():
        return list(networks.available_networks.keys())
    
    import entry_point
    entry_point.main(app)

script_callbacks.on_app_started(api_networks)
script_callbacks.on_before_ui(before_ui)
