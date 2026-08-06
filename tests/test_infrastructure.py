from pathlib import Path

import yaml


def _documents(path: str) -> list[dict]:
    return list(yaml.safe_load_all(Path(path).read_text(encoding="utf-8")))


def test_training_job_storage_mounts_and_resources() -> None:
    documents = _documents("k8s/training-job.yaml")
    assert [document["kind"] for document in documents] == [
        "PersistentVolumeClaim",
        "PersistentVolumeClaim",
        "Job",
    ]
    job = documents[2]
    pod_spec = job["spec"]["template"]["spec"]
    container = pod_spec["containers"][0]
    mounts = {mount["mountPath"] for mount in container["volumeMounts"]}
    assert {"/app/configs", "/app/data", "/app/checkpoints"} <= mounts
    assert container["resources"]["requests"] == {"cpu": "2", "memory": "4Gi"}
    assert container["resources"]["limits"] == {"cpu": "2", "memory": "4Gi"}
    assert container["imagePullPolicy"] == "IfNotPresent"


def test_serving_deployment_matches_rubric() -> None:
    deployment = _documents("k8s/serving-deployment.yaml")[0]
    spec = deployment["spec"]
    container = spec["template"]["spec"]["containers"][0]
    assert spec["replicas"] == 2
    assert spec["strategy"]["rollingUpdate"] == {
        "maxSurge": 1,
        "maxUnavailable": 0,
    }
    assert container["livenessProbe"]["httpGet"]["path"] == "/health"
    assert container["livenessProbe"]["periodSeconds"] == 10
    assert container["livenessProbe"]["failureThreshold"] == 3
    assert container["readinessProbe"]["periodSeconds"] == 5
    assert container["readinessProbe"]["initialDelaySeconds"] == 15
    assert container["resources"]["requests"] == {
        "cpu": "500m",
        "memory": "1Gi",
    }
    assert container["resources"]["limits"] == {"cpu": "1", "memory": "2Gi"}
    checkpoint_mount = next(
        mount
        for mount in container["volumeMounts"]
        if mount["mountPath"] == "/app/checkpoints"
    )
    assert checkpoint_mount["readOnly"] is True


def test_service_and_hpa_match_rubric() -> None:
    service = _documents("k8s/serving-service.yaml")[0]
    assert service["spec"]["type"] == "ClusterIP"
    assert service["spec"]["ports"][0]["port"] == 80
    assert service["spec"]["ports"][0]["targetPort"] == 8080

    hpa = _documents("k8s/hpa.yaml")[0]
    assert hpa["apiVersion"] == "autoscaling/v2"
    assert hpa["spec"]["minReplicas"] == 2
    assert hpa["spec"]["maxReplicas"] == 5
    assert hpa["spec"]["metrics"][0]["resource"]["target"][
        "averageUtilization"
    ] == 70


def test_dockerfiles_match_rubric() -> None:
    training = Path("docker/Dockerfile.train").read_text(encoding="utf-8")
    serving = Path("docker/Dockerfile.serve").read_text(encoding="utf-8")
    assert training.count("FROM ") == 2
    assert "CONFIG_PATH=/app/configs/training_config.yaml" in training
    assert 'ENTRYPOINT ["python", "-m", "src.train"]' in training
    assert "EXPOSE 8080" in serving
    assert "USER app" in serving
    assert "HEALTHCHECK" in serving

