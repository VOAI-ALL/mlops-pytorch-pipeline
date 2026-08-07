from pathlib import Path

import pytest
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from src.train import evaluate, load_config, train_one_epoch
from src import train as train_module


def _loader() -> DataLoader:
    torch.manual_seed(7)
    inputs = torch.randn(8, 3, 4, 4)
    targets = torch.tensor([0, 1, 0, 1, 0, 1, 0, 1])
    return DataLoader(TensorDataset(inputs, targets), batch_size=4)


def test_training_and_evaluation_return_metrics() -> None:
    model = nn.Sequential(nn.Flatten(), nn.Linear(3 * 4 * 4, 2))
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
    criterion = nn.CrossEntropyLoss()
    device = torch.device("cpu")

    train_loss, train_accuracy = train_one_epoch(
        model, _loader(), optimizer, criterion, device
    )
    val_loss, val_accuracy = evaluate(model, _loader(), criterion, device)

    assert train_loss > 0
    assert val_loss > 0
    assert 0 <= train_accuracy <= 1
    assert 0 <= val_accuracy <= 1


def test_load_config_requires_all_sections(tmp_path: Path) -> None:
    config = tmp_path / "invalid.yaml"
    config.write_text("model: {}\n", encoding="utf-8")
    with pytest.raises(ValueError, match="missing sections"):
        load_config(config)


def test_load_config_accepts_project_config() -> None:
    config = load_config("configs/training_config.yaml")
    assert config["model"]["architecture"] == "resnet18"
    assert config["data"]["dataset"] == "cifar10"


def test_train_saves_checkpoint_and_stops_early(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    model = nn.Sequential(nn.Flatten(), nn.Linear(3 * 4 * 4, 2))
    loader = _loader()
    monkeypatch.setattr(train_module, "get_model", lambda **_: model)
    monkeypatch.setattr(train_module, "get_dataloaders", lambda **_: (loader, loader))
    monkeypatch.setattr(train_module, "train_one_epoch", lambda *args: (0.8, 0.5))
    validation_results = iter([(0.7, 0.6), (0.7, 0.6)])
    monkeypatch.setattr(
        train_module, "evaluate", lambda *args: next(validation_results)
    )
    config = {
        "model": {"architecture": "resnet18", "num_classes": 2},
        "training": {
            "epochs": 4,
            "batch_size": 4,
            "learning_rate": 0.001,
            "early_stopping_patience": 1,
        },
        "data": {"dataset": "cifar10", "data_dir": str(tmp_path)},
        "output": {
            "checkpoint_dir": str(tmp_path),
            "model_name": "test.pt",
        },
    }

    checkpoint_path = train_module.train(config)
    checkpoint = torch.load(checkpoint_path, weights_only=False)
    output = capsys.readouterr().out

    assert checkpoint_path.is_file()
    assert checkpoint["architecture"] == "resnet18"
    assert checkpoint["num_classes"] == 2
    assert '"event": "checkpoint_saved"' in output
    assert '"event": "early_stopping"' in output
