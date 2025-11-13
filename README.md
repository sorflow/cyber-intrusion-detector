# AI Cybersecurity Intrusion Detector

Production-leaning version of the CICIDS-2017 intrusion detector. It now includes a configurable training pipeline, experiment tracking, versioned model artifacts, and deployment-ready FastAPI + Streamlit services.

---

## 1. Environment & Tooling

```bash
python -m venv .venv && .venv\Scripts\activate  # Windows example
pip install --upgrade pip
pip install -r requirements.txt
# or, if you prefer Conda:
conda env create -f environment.yml
conda activate ai-cyber-intrusion-detector
```

The `requirements.txt` file pins the exact runtime packages; `environment.yml` mirrors the same stack for Conda users.

---

## 2. Reproducible Training (Config + Notebook)

All training is configuration driven:

```bash
python src/train_supervised.py --config configs/train_default.yaml
```

Key features:

- **YAML configs** control dataset paths, split ratios, and RandomForest hyper-parameters.
- **MLflow logging** (automatic) sends params, metrics, confusion matrices, and artifacts to `mlruns/`.
- **Model registry** automatically tracks metadata in `src/models/model_registry.json`.
- **Versioned artifacts** are stored under `src/models/rf-<timestamp>.joblib` while the API still consumes `src/models/rf.pk1`.

Prefer notebooks? Open `notebooks/training_pipeline.ipynb` to run the exact same pipeline interactively and inspect the registry tail.

```bash
jupyter lab notebooks/training_pipeline.ipynb
```

> Launch `mlflow ui --backend-store-uri mlruns` in another terminal to browse experiment history.

---

## 3. Serving & Live Dashboard

```bash
# FastAPI scoring service
python src/serve.py  # serves on http://127.0.0.1:8000 by default

# Streamlit telemetry dashboard
streamlit run src/dashboard/app.py
```

The dashboard sidebar lets you point at any FastAPI URL, stream CICIDS CSV rows, view confidence trends, and export predictions to `dashboard/logs.csv`.

---

## 4. Deployment & Portfolio Tips

- **Containerize** the FastAPI app and dashboard (multi-stage Dockerfile) → deploy to Railway, Render, or AWS Lightsail. Use environment variables for the model path + host.
- **Expose monitoring**: publish the MLflow tracking server (read-only) or capture screenshots in the README.
- **Record a short Loom/video** walking through training, API testing (via `/docs`), and the dashboard's alerting workflow.
- **Extend threat coverage**: add configs trained on other CICIDS attack files; highlight how the registry separates models per attack profile.
- **Security narrative**: document how to feed NetFlow, PCAP, or SIEM exports to the pipeline and how the model could become part of a SOC automation stack.

---

## 5. Project Map

```
├── configs/
│   └── train_default.yaml        # parameterized training config
├── notebooks/
│   └── training_pipeline.ipynb   # reproducible notebook entry-point
├── src/
│   ├── dashboard/                # Streamlit UI
│   ├── models/
│   │   ├── model_registry.json   # version + metadata log
│   │   └── rf.pk1                # latest bundle consumed by FastAPI
│   ├── features.py               # preprocessing helpers
│   ├── serve.py                  # FastAPI inference server
│   └── train_supervised.py       # config-driven training script
└── data/                         # CICIDS-2017 CSVs (not tracked in git)
```

This setup gives reviewers a clear story: configurable data science workflow → experiment tracking → deployable inference stack → polished dashboard + documentation.
