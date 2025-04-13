from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import io

app = FastAPI()

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))  # Verifies it's a valid image

        # PLACEHLDER FOR IMAGE PROCESSING
        print("Image received and opened successfully.")

        return JSONResponse(content={
            "success": True,
            "filename": file.filename,
            "message": "Image upload and parsing successful."
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={
            "success": False,
            "error": str(e)
        })