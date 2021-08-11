from typing import Optional

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/importfile/")
async def import_file(file: UploadFile = File(...)):
    return {"filename": file.filename}
