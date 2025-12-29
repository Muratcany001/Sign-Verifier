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

tf.config.threading.set_intra_op_parallelism_threads(1)
tf.config.threading.set_inter_op_parallelism_threads(1)
print("Model yükleniyor...")

def create_lambda_call(tf_module):
    def lambda_call(inputs, mask=None, training=None):
        return tf_module.abs(inputs[0] - inputs[1])
    return lambda_call

try:
    model = load_model("trained_model.h5", safe_mode=False, custom_objects={"tf": tf})

    for layer in model.layers:
        if isinstance(layer, tf.keras.layers.Lambda):
            layer.call = create_lambda_call(tf)

    model.summary()
    print(" Model başarıyla yüklendi!")
except Exception as e:
    print(" Model yüklenemedi:", e)
    raise

## Modelin öğrenmesini kolaylaştırmak için normalizasyon
def prepare_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((112, 112))
    img_array = img_to_array(img) / 255.0
    return np.expand_dims(img_array, axis=0)


@app.post("/api/verify")
async def verify_signature(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
    try:
        print(f"\n=== KARŞILAŞTIRMA: {file1.filename} vs {file2.filename} ===")

        img1 = prepare_image(await file1.read())
        img2 = prepare_image(await file2.read())

        pred = model.predict([img1, img2], verbose=0)
        similarity_score = float(pred[0][0])

        print(f"Sigmoid output: {similarity_score:.4f}")

        if similarity_score > 0.9:
            message = "İmza benzerliği: ÇOK YÜKSEK (aynı kişi)"
            confidence = "çok yüksek"
            is_match = True
        elif similarity_score > 0.75:
            message = "İmza benzerliği: YÜKSEK"
            confidence = "yüksek"
            is_match = True
        elif similarity_score > 0.6:
            message = "İmza benzerliği: ORTA (manuel kontrol)"
            confidence = "orta"
            is_match = False
        else:
            message = "İmza benzerliği: DÜŞÜK (farklı kişiler)"
            confidence = "düşük"
            is_match = False

        return {
            "success": True,
            "similarity_score": round(similarity_score, 4),
            "is_match": is_match,
            "confidence": confidence,
            "message": message
        }

    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": str(e),
            "detail": traceback.format_exc()
        }


@app.get("/")
async def root():
    return {"message": "İmza Doğrulama API - SIGMOID MODE"}


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
