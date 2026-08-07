"""Train a CIFAR-10 classifier from a YAML configuration file."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

import torch
import torch.nn as nn
import yaml
from torch.utils.data import DataLoader

from src.dataset import CIFAR10_CLASSES, get_dataloaders
from src.model import get_model


def load_config(config_path: str | Path) -> dict[str, Any]:
    path = Path(config_path)
    if not path.is_file():
        raise FileNotFoundError(f"Training configuration not found: {path}")
    with path.open(encoding="utf-8") as stream:
        config = yaml.safe_load(stream)
    required = {"model", "training", "data", "output"}
    if not isinstance(config, dict) or not required.issubset(config):
        missing = required - set(config or {})
        raise ValueError(f"Configuration is missing sections: {sorted(missing)}")
    if config["data"].get("dataset", "").lower() != "cifar10":
        raise ValueError("Only the cifar10 dataset is supported")
    return config


def _run_loader(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
    optimizer: torch.optim.Optimizer | None,
) -> tuple[float, float]:
    training = optimizer is not None
    model.train(training)
    total_loss = 0.0
    correct = 0
    total = 0

    context = torch.enable_grad() if training else torch.no_grad()
    with context:
        for inputs, targets in loader:
            inputs = inputs.to(device, non_blocking=True)
            targets = targets.to(device, non_blocking=True)
            if optimizer is not None:
                optimizer.zero_grad(set_to_none=True)
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            if optimizer is not None:
                loss.backward()
                optimizer.step()
            total_loss += loss.item() * inputs.size(0)
            correct += outputs.argmax(dim=1).eq(targets).sum().item()
            total += targets.size(0)

    if total == 0:
        raise ValueError("Cannot calculate metrics for an empty data loader")
    return total_loss / total, correct / total


def train_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    device: torch.device,
) -> tuple[float, float]:
    return _run_loader(model, loader, criterion, device, optimizer)


def evaluate(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
) -> tuple[float, float]:
    return _run_loader(model, loader, criterion, device, None)


def train(config: dict[str, Any]) -> Path:
    model_config = config["model"]
    training_config = config["training"]
    data_config = config["data"]
    output_config = config["output"]

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(json.dumps({"event": "training_started", "device": str(device)}), flush=True)

    model = get_model(
        architecture=model_config["architecture"],
        num_classes=int(model_config["num_classes"]),
    ).to(device)
    train_loader, val_loader = get_dataloaders(
        data_dir=data_config["data_dir"],
        batch_size=int(training_config["batch_size"]),
        num_workers=int(data_config.get("num_workers", 2)),
        max_train_samples=data_config.get("max_train_samples"),
        max_val_samples=data_config.get("max_val_samples"),
    )
    optimizer = torch.optim.Adam(
        model.parameters(), lr=float(training_config["learning_rate"])
    )
    criterion = nn.CrossEntropyLoss()
    checkpoint_dir = Path(output_config["checkpoint_dir"])
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = checkpoint_dir / output_config["model_name"]

    best_val_loss = float("inf")
    patience_counter = 0
    patience = int(training_config["early_stopping_patience"])
    if patience <= 0:
        raise ValueError("early_stopping_patience must be positive")

    for epoch in range(1, int(training_config["epochs"]) + 1):
        train_loss, train_accuracy = train_one_epoch(
            model, train_loader, optimizer, criterion, device
        )
        val_loss, val_accuracy = evaluate(model, val_loader, criterion, device)
        print(
            json.dumps(
                {
                    "epoch": epoch,
                    "train_loss": round(train_loss, 4),
                    "train_accuracy": round(train_accuracy, 4),
                    "val_loss": round(val_loss, 4),
                    "val_accuracy": round(val_accuracy, 4),
                }
            ),
            flush=True,
        )

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            class_names = list(CIFAR10_CLASSES[: int(model_config["num_classes"])])
            torch.save(
                {
                    "epoch": epoch,
                    "architecture": model_config["architecture"],
                    "num_classes": int(model_config["num_classes"]),
                    "class_names": class_names,
                    "model_state_dict": model.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                    "val_loss": val_loss,
                    "val_accuracy": val_accuracy,
                },
                checkpoint_path,
            )
            print(
                json.dumps(
                    {"event": "checkpoint_saved", "path": str(checkpoint_path)}
                ),
                flush=True,
            )
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(
                    json.dumps({"event": "early_stopping", "epoch": epoch}),
                    flush=True,
                )
                break

    print(
        json.dumps(
            {"event": "training_complete", "best_val_loss": round(best_val_loss, 4)}
        ),
        flush=True,
    )
    return checkpoint_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        default=os.getenv("CONFIG_PATH", "configs/training_config.yaml"),
        help="YAML configuration path (default: CONFIG_PATH or configs/training_config.yaml)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    train(load_config(args.config))


if __name__ == "__main__":
    main()
