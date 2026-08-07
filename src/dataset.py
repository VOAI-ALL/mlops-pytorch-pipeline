"""CIFAR-10 transforms and data loader construction."""

from __future__ import annotations

from pathlib import Path

import torch
from torch.utils.data import DataLoader, Dataset, Subset
from torchvision import datasets, transforms

CIFAR10_CLASSES = (
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck",
)
CIFAR10_MEAN = (0.4914, 0.4822, 0.4465)
CIFAR10_STD = (0.2470, 0.2435, 0.2616)


def get_transforms(train: bool = True) -> transforms.Compose:
    operations: list[object] = []
    if train:
        operations.extend(
            [
                transforms.RandomHorizontalFlip(),
                transforms.RandomCrop(32, padding=4),
            ]
        )
    operations.extend(
        [
            transforms.ToTensor(),
            transforms.Normalize(CIFAR10_MEAN, CIFAR10_STD),
        ]
    )
    return transforms.Compose(operations)


def _limit_dataset(dataset: Dataset, maximum: int | None) -> Dataset:
    if maximum is None:
        return dataset
    if maximum <= 0:
        raise ValueError("Dataset sample limits must be positive")
    return Subset(dataset, range(min(maximum, len(dataset))))


def get_dataloaders(
    data_dir: str | Path,
    batch_size: int = 64,
    num_workers: int = 2,
    max_train_samples: int | None = None,
    max_val_samples: int | None = None,
) -> tuple[DataLoader, DataLoader]:
    """Download CIFAR-10 if needed and return training/validation loaders."""
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")

    train_dataset = datasets.CIFAR10(
        root=str(data_dir),
        train=True,
        download=True,
        transform=get_transforms(train=True),
    )
    val_dataset = datasets.CIFAR10(
        root=str(data_dir),
        train=False,
        download=True,
        transform=get_transforms(train=False),
    )
    train_dataset = _limit_dataset(train_dataset, max_train_samples)
    val_dataset = _limit_dataset(val_dataset, max_val_samples)
    pin_memory = torch.cuda.is_available()

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )
    return train_loader, val_loader

