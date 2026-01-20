# Sign-Verifier

A simple signature verification project:
- Backend: FastAPI service that loads a Keras model (imza_modeli.h5) and exposes an endpoint to compare two signature images.
- Frontend: Angular (v21) single-page application located in frontend/signVerifierFrontend for interacting with the service.
- Model & Notebook: A trained model (imza_modeli.h5) and a Jupyter notebook (imza-dogrulama-with-cnn.ipynb) used for training/experiments.

---

## Features

- Signature similarity scoring using a pre-trained Keras model.
- REST API endpoint for file upload and verification.
- Small Angular frontend to demo the verification workflow.
- Reproducible training notebook included.

---

## Architecture / How it works

- The backend (main.py) loads `imza_modeli.h5` and exposes POST /api/verify.
- /api/verify accepts two files (`file1`, `file2`), performs preprocessing (RGB convert, resize to 112×112, normalize), runs the model and returns a similarity score and a boolean `is_match`.
- The Angular frontend can call the backend to upload two images and display results.

---

## Prerequisites

- Python 3.8+ (match the TensorFlow version used to train the model)
- Node.js 18+ and npm (for the frontend)
- Enough RAM / optional GPU (TensorFlow may require significant resources)

Recommended Python packages (install into a virtual environment):
- fastapi
- uvicorn
- tensorflow (or tensorflow-cpu)
- pillow
- numpy

Example (use an isolated venv):
```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate     # Windows (PowerShell)
pip install --upgrade pip
pip install fastapi uvicorn pillow numpy tensorflow
```

Note: TensorFlow installation can vary by OS and whether you want GPU support. For many setups, `tensorflow` or `tensorflow-cpu` from PyPI will work.

---

## Backend — Run locally

1. Ensure `imza_modeli.h5` is present in the repository root (it is included here).
2. Start the API:
```bash
# from project root
# activate your venv first
python main.py
# or explicitly with uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

- By default the API serves at: http://localhost:8000
- Endpoint: POST http://localhost:8000/api/verify

API response format (example):
```json
{
  "success": true,
  "similarity_score": 0.7324,
  "is_match": true,
  "message": "İmza benzerliği: YÜKSEK"
}
```
If an error occurs:
```json
{"success": false, "error": "error details..."}
```

Important notes about the server code:
- main.py preprocesses images by resizing to 112×112, converting to RGB, normalizing to [0,1].
- The model returns a single similarity score; the code uses `is_match = score > 0.5`.
- CORS is allowed from all origins for easy local frontend development.

---

## API usage examples

Curl:
```bash
curl -X POST "http://localhost:8000/api/verify" \
  -F "file1=@/path/to/signature1.png" \
  -F "file2=@/path/to/signature2.png"
```

JavaScript (fetch):
```js
const formData = new FormData();
formData.append('file1', fileInput1.files[0]);
formData.append('file2', fileInput2.files[0]);

fetch('http://localhost:8000/api/verify', {
  method: 'POST',
  body: formData
})
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.error(err));
```

---

## Frontend — Run locally

The frontend is inside `frontend/signVerifierFrontend`.

1. Install dependencies and run:
```bash
cd frontend/signVerifierFrontend
npm install
npm start      # runs `ng serve` (development server)
```

2. Open the app in your browser:
```
http://localhost:4200
```

Build for production:
```bash
npm run build
# build artifacts will be under `dist/` by Angular defaults
```

Run frontend unit tests:
```bash
npm test
# this project uses Vitest via Angular CLI setup
```

---

## Model & Training

- The trained model file: `imza_modeli.h5` — this is used by the backend for inference.
- Training notebook: `imza-dogrulama-with-cnn.ipynb` contains the dataset exploration, model architecture and training code used to produce the model.

If you want to retrain:
- Open the notebook in Jupyter / Colab.
- Ensure the dataset paths and versions of TensorFlow are compatible.
- Export a new HDF5 model and replace `imza_modeli.h5` (or change the load path in `main.py`).

---

## Development notes & Troubleshooting

- Model loading errors:
  - Ensure `imza_modeli.h5` exists in the same directory as `main.py`, or update the path in `main.py`.
  - TensorFlow/Keras version mismatches can cause load errors. Use the same TF version that was used to train the model if possible.
  - If you see Lambda-layer problems, the code attempts to patch Lambda layers; inspect traceback for details.

- Memory / performance:
  - TensorFlow models can be large. If you run into memory issues, try `tensorflow-cpu` or use a machine with more RAM / GPU.

- If the server doesn't start:
  - Check the console output for traceback and any missing library errors.
  - Confirm the Python virtual environment is active and dependencies are installed.

- Security:
  - Current CORS setting allows all origins (convenient for dev). For production, limit allowed origins and secure file upload endpoints appropriately.
  - Be careful exposing a model that may include sensitive data or can be abused.

---

## Contributing

Contributions welcome. Suggested steps:
1. Fork the repository.
2. Create a feature branch: git checkout -b feat/your-feature
3. Add tests (if applicable) and update docs.
4. Open a pull request describing your changes.

Please include details about:
- how you tested the model / API
- package / TF versions used

---

## License

This repository does not include a license file. Add a LICENSE to define how this project may be used.

---

If you want, I can:
- Add a minimal requirements.txt and a simple systemd/Procfile example for running the backend in production.
- Create a basic README for the Angular frontend inside its folder (or update the existing one).
- Add a Dockerfile for the backend to make deployment easier.
