"""FastAPI model-serving application."""

from __future__ import annotations

import io
import os
import pickle
from pathlib import Path
from typing import Any

import torch
from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

from src.dataset import CIFAR10_CLASSES, get_transforms
from src.model import get_model

DEFAULT_MODEL_PATH = "/app/checkpoints/classifier_v1.pt"


class ModelService:
    def __init__(self, model_path: str | Path) -> None:
        self.model_path = Path(model_path)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model: torch.nn.Module | None = None
        self.class_names = list(CIFAR10_CLASSES)
        self.load_error: str | None = None
        self._load()

    def _load(self) -> None:
        try:
            checkpoint = torch.load(
                self.model_path, map_location=self.device, weights_only=True
            )
            architecture = checkpoint.get("architecture", "resnet18")
            num_classes = int(checkpoint.get("num_classes", 10))
            model = get_model(architecture, num_classes)
            model.load_state_dict(checkpoint["model_state_dict"])
            model.to(self.device).eval()
            self.model = model
            class_names = checkpoint.get(
                "class_names", list(CIFAR10_CLASSES[:num_classes])
            )
            if len(class_names) != num_classes:
                raise ValueError("Checkpoint class_names do not match num_classes")
            self.class_names = class_names
        except (
            OSError,
            EOFError,
            pickle.UnpicklingError,
            KeyError,
            RuntimeError,
            ValueError,
        ) as exc:
            self.load_error = str(exc)

    @property
    def loaded(self) -> bool:
        return self.model is not None

    @torch.inference_mode()
    def predict(self, image: Image.Image) -> dict[str, Any]:
        if self.model is None:
            raise RuntimeError(self.load_error or "Model is not loaded")
        tensor = get_transforms(train=False)(image.convert("RGB")).unsqueeze(0)
        probabilities = torch.softmax(self.model(tensor.to(self.device)), dim=1)[0]
        values = probabilities.cpu().tolist()
        predicted_index = int(probabilities.argmax().item())
        return {
            "predicted_class": self.class_names[predicted_index],
            "predicted_index": predicted_index,
            "confidence": values[predicted_index],
            "probabilities": {
                name: probability
                for name, probability in zip(self.class_names, values, strict=True)
            },
        }


def create_app(model_path: str | Path | None = None) -> FastAPI:
    app = FastAPI(title="CIFAR-10 Model Service", version="1.0.0")
    app.state.model_service = ModelService(
        model_path or os.getenv("MODEL_PATH", DEFAULT_MODEL_PATH)
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        service: ModelService = app.state.model_service
        if not service.loaded:
            raise HTTPException(
                status_code=503,
                detail={"status": "unhealthy", "reason": service.load_error},
            )
        return {"status": "healthy", "model": service.model_path.name}

    @app.post("/predict")
    async def predict(image: UploadFile = File(...)) -> dict[str, Any]:
        service: ModelService = app.state.model_service
        if not service.loaded:
            raise HTTPException(status_code=503, detail="Model is not loaded")
        if image.content_type is None or not image.content_type.startswith("image/"):
            raise HTTPException(status_code=415, detail="Upload must be an image")
        try:
            payload = await image.read()
            pil_image = Image.open(io.BytesIO(payload))
            pil_image.load()
        except (UnidentifiedImageError, OSError):
            raise HTTPException(status_code=400, detail="Invalid image data") from None
        return service.predict(pil_image)

    return app


app = create_app()
