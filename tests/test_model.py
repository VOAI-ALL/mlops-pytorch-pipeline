import pytest
import torch

from src.model import get_model


def test_resnet18_output_shape() -> None:
    model = get_model("resnet18", num_classes=10)
    output = model(torch.randn(2, 3, 32, 32))
    assert output.shape == (2, 10)


def test_resnet18_uses_cifar_stem() -> None:
    model = get_model("resnet18", num_classes=10)
    assert model.conv1.kernel_size == (3, 3)
    assert model.conv1.stride == (1, 1)
    assert isinstance(model.maxpool, torch.nn.Identity)


def test_rejects_unknown_architecture() -> None:
    with pytest.raises(ValueError, match="Unsupported architecture"):
        get_model("unknown", num_classes=10)

