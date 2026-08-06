"""Model construction utilities for CIFAR-10 classification."""

from __future__ import annotations

import torch.nn as nn
from torchvision.models import resnet18


def get_model(architecture: str = "resnet18", num_classes: int = 10) -> nn.Module:
    """Create a CIFAR-sized ResNet-18.

    The standard ImageNet stem downsamples 32x32 inputs too aggressively. A 3x3,
    stride-1 convolution and no max pool preserve spatial detail for CIFAR-10.
    """
    if architecture.lower() != "resnet18":
        raise ValueError(f"Unsupported architecture: {architecture!r}")
    if num_classes < 2:
        raise ValueError("num_classes must be at least 2")

    model = resnet18(weights=None)
    model.conv1 = nn.Conv2d(
        3, 64, kernel_size=3, stride=1, padding=1, bias=False
    )
    model.maxpool = nn.Identity()
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    return model

