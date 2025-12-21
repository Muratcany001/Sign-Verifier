import uvicorn
import numpy as np
import io
import tensorflow as tf
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import builtins
if not hasattr(builtins, 'tf'):
    builtins.tf = tf

print("Model yükleniyor...")
try:
    model = load_model('imza_modeli.h5', safe_mode=False, custom_objects={'tf': tf})
    for layer in model.layers:
        if isinstance(layer, tf.keras.layers.Lambda):
            layer.call = lambda inputs, mask=None, training=None, tf_ref=tf: tf_ref.abs(inputs[0] - inputs[1])
    
    print("Model başarıyla yüklendi!")
except Exception as e:
    print(f"Model yüklenirken hata oluştu: {e}")
    import traceback
    traceback.print_exc()
    raise



def prepare_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((112, 112))
    img_array = img_to_array(img)
    img_array = img_array / 255.0
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

        # 1. Tahmin Yap
        prediction = model.predict([processed_img1, processed_img2], verbose=0)
        score = float(prediction[0][0])

        is_match = score > 0.5 

        message = "İmza benzerliği: YÜKSEK" if is_match else "imza benzerliği: ORTA"

        return {
            "success": True,
            "similarity_score": score,
            "is_match": is_match, 
            "message": message
        }

    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)