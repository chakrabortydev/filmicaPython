from fastapi import FastAPI, UploadFile, File, HTTPException
from screenplay_pdf_to_json import convert
from io import BytesIO
import uvicorn

app = FastAPI()

@app.post("/process")
async def process_file(file: UploadFile = File(...)):
    try:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        # Read the file's bytes
        file_bytes = await file.read()

        # Wrap the bytes in a BytesIO object
        file_like = BytesIO(file_bytes)

        # Call the convert function
        scriptJSON = convert(file_like, 0)

        return scriptJSON
    except Exception as e:
        print("Error in processing:", e)
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
