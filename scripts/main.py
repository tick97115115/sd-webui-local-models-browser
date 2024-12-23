from modules import ui_extra_networks, script_callbacks, shared

import gradio as gr
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

class ExtraNetworksPageCustom(ui_extra_networks.ExtraNetworksPage):
    def __init__(self):
        super().__init__('MyCustomTab')  # Set the tab name
        self.allow_negative_prompt = True  # Optional: Enable integration with negative prompts

    def create_item(self, name, index=None, enable_filter=True):
        return

    def list_items(self):
        return
    
    def create_html(self, tabname, *, empty=False):
        fastapi_endpoint = f'/local-models-browser'
        return f'<iframe src="{fastapi_endpoint}" width="100%" height="500px" style="border:none;"></iframe>'


    # def create_ui(self, *args, **kwargs):
    #     """
    #     Override this method to define your tab's UI.
    #     Use the Gradio components here to build the interface.
    #     """
    #     with self.block:
    #         gr.Markdown("### My Custom Tab")
            
    #         # Example UI components
    #         input_box = gr.Textbox(label="Enter Custom Data")
    #         output_box = gr.Textbox(label="Processed Output")
    #         process_button = gr.Button("Process")

    #         def process_input(input_data):
    #             return f"Processed: {input_data}"

    #         # Hook up processing logic
    #         process_button.click(process_input, inputs=[input_box], outputs=[output_box])

def before_ui():
    """Register your custom tab."""
    ui_extra_networks.register_page(ExtraNetworksPageCustom())

def api_networks(_: gr.Blocks, app: FastAPI):

    from os.path import join, dirname
    flutter_build_dir = join(dirname(dirname(__file__)), "ui", "build", "web")
    print(f"flutter_build_dir: {flutter_build_dir}")
    html_path = join(flutter_build_dir, "index.html")
    app.mount("/local-models-browser", StaticFiles(directory=flutter_build_dir, html=True), name="local-models-browser-static")
    # @app.get("/sdapi/v1/loras")
    # async def get_loras():
    #     return [create_lora_json(obj) for obj in networks.available_networks.values()]

    # @app.post("/sdapi/v1/refresh-loras")
    # async def refresh_loras():
    #     return networks.list_available_networks()

    # @app.get("/local-models-browser/api/v1/loras")
    @app.get("/local-models-browser")
    async def home():
        return FileResponse(html_path, media_type="text/html")


script_callbacks.on_app_started(api_networks)
script_callbacks.on_before_ui(before_ui)