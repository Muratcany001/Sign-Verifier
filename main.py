
import uvicorn
import numpy as np
import io
import tensorflow as tf
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Model yükleniyor...")
try:
    model = load_model("imza_modeli.h5")
    print("Model başarıyla yüklendi!")
except Exception as e:
    print(f"Model yüklenirken hata oluştu: {e}")


def prepare_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((112, 112))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

@app.post("/api/verify")
async def verify_signature(
    file1: UploadFile = File(...), 
    file2: UploadFile = File(...)
):
    try:
        img1_bytes = await file1.read()
        img2_bytes = await file2.read()

        processed_img1 = prepare_image(img1_bytes)
        processed_img2 = prepare_image(img2_bytes)

        # 3. Modele sordugumuz bolum 
        prediction = model.predict([processed_img1, processed_img2])
        score = float(prediction[0][0])

        is_match = score > 0.5 

        return {
            "success": True,
            "similarity_score": score,
            "is_match": is_match, 
            "message": "İmzalar eşleşiyor" if is_match else "İmzalar uyuşmuyor"
        }

    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)