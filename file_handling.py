# poetry add python-multipart
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles


import shutil 
import os
UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True) # makes folder
app = FastAPI()
app.mount("/static", StaticFiles(directory=UPLOAD_FOLDER), name="static")


# below code allows user to upload file on the app and it shows here in uploads folder
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Create a full file path in the static folder
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save the uploaded file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # URL that can be used to access the file
    file_url = f"/static/{file.filename}"

    return {
        "filename": file.filename,
        "file_url": file_url
    }