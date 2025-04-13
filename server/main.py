import os
import io
import json
from datetime import datetime

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from PIL import Image
from dotenv import load_dotenv

from utils import process_image_for_json, create_circuit_diagram

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI()

data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)


@app.get("/")
async def root():
    return {"message": "Hello! Circulens API is running."}


@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_extension = os.path.splitext(
            file.filename)[1] if '.' in file.filename else '.png'
        image_filename = f'{timestamp}{file_extension}'
        image_path = os.path.join(data_dir, image_filename)

        image.save(image_path)

        analysis_result = process_image_for_json(
            image_path=image_path,
            json_schema={
                "type": "object",
                "properties": {
                    "resistors": {"type": "integer"},
                    "resistor_value": {"type": "string"},
                    "leds": {"type": "integer"},
                    "led_colors": {
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "grounding": {"type": "boolean"}
                },
                "required": ["resistors", "resistor_value", "leds", "led_colors", "grounding"]
            },
            api_key=GEMINI_API_KEY
        )

        json_data = json.dumps(analysis_result)
        circuit_diagram_path = create_circuit_diagram(json_data)
        diagram_filename = os.path.basename(circuit_diagram_path)

        return JSONResponse(content={
            "success": True,
            "message": "Image uploaded and processed successfully.",
            "analysis_result": analysis_result,
            "circuit_diagram": diagram_filename,
            "diagram_path": circuit_diagram_path
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={
            "success": False,
            "error": str(e)
        })


@app.get("/diagrams/{filename}")
async def get_diagram(filename: str):
    file_path = os.path.join("results", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return JSONResponse(
        status_code=404,
        content={"message": f"Diagram {filename} not found"}
    )
