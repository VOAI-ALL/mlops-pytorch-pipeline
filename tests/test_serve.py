import io
from pathlib import Path

import torch
from fastapi.testclient import TestClient
from PIL import Image

from src.dataset import CIFAR10_CLASSES
from src.model import get_model
from src.serve import create_app


def _write_checkpoint(path: Path) -> None:
    model = get_model("resnet18", 10)
    torch.save(
        {
            "architecture": "resnet18",
            "num_classes": 10,
            "class_names": list(CIFAR10_CLASSES),
            "model_state_dict": model.state_dict(),
        },
        path,
    )


def _png_bytes() -> bytes:
    stream = io.BytesIO()
    Image.new("RGB", (32, 32), color=(50, 100, 150)).save(stream, format="PNG")
    return stream.getvalue()


def test_health_is_unavailable_without_checkpoint(tmp_path: Path) -> None:
    client = TestClient(create_app(tmp_path / "missing.pt"))
    response = client.get("/health")
    assert response.status_code == 503


def test_health_is_unavailable_with_invalid_checkpoint(tmp_path: Path) -> None:
    checkpoint = tmp_path / "invalid.pt"
    checkpoint.write_bytes(b"not a torch checkpoint")
    client = TestClient(create_app(checkpoint))
    assert client.get("/health").status_code == 503


def test_health_and_prediction_with_checkpoint(tmp_path: Path) -> None:
    checkpoint = tmp_path / "model.pt"
    _write_checkpoint(checkpoint)
    client = TestClient(create_app(checkpoint))

    assert client.get("/health").status_code == 200
    response = client.post(
        "/predict", files={"image": ("test.png", _png_bytes(), "image/png")}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["predicted_class"] in CIFAR10_CLASSES
    assert len(body["probabilities"]) == 10
    assert abs(sum(body["probabilities"].values()) - 1.0) < 1e-5


def test_predict_rejects_non_image(tmp_path: Path) -> None:
    checkpoint = tmp_path / "model.pt"
    _write_checkpoint(checkpoint)
    client = TestClient(create_app(checkpoint))
    response = client.post(
        "/predict", files={"image": ("test.txt", b"not an image", "text/plain")}
    )
    assert response.status_code == 415
