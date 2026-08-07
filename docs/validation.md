# End-to-End Validation Record

Validation was performed on Windows using the `MLDL` Conda environment, Docker
Desktop, and Docker Desktop Kubernetes in `kind` mode.

## Environment

- [x] `conda activate MLDL`
- [x] Python 3.12.13
- [x] PyTorch 2.12.0+cpu and torchvision 0.27.0+cpu
- [x] Docker 29.5.3
- [x] kubectl client 1.34.1
- [x] Docker Desktop Kubernetes 1.34.3 with a Ready `kind` control-plane node

## Local application

- [x] `python -m pytest -q` passes all 16 tests.
- [x] Smoke training emits structured JSON metrics.
- [x] Smoke training creates `classifier_smoke.pt`.
- [x] Local `/health` returns HTTP 200 with the checkpoint loaded.
- [x] Local `/predict` returns ten probabilities summing approximately to one.

Evidence:

| Check | Evidence |
|---|---|
| Unit tests | [01-unit-tests.png](evidence/01-unit-tests.png) |
| Local smoke training | [02-local-smoke-training.png](evidence/02-local-smoke-training.png) |
| Local health and prediction | [03-local-api-validation.png](evidence/03-local-api-validation.png) |

## Docker

- [x] `mlops-train:v1` builds successfully as a Linux/AMD64 image.
- [x] Mounted container training creates a host checkpoint.
- [x] `mlops-serve:v1` builds successfully as a Linux/AMD64 image.
- [x] Serving container reports user `app` and health `healthy`.
- [x] Container `/health` returns HTTP 200.
- [x] Container `/predict` succeeds with `test_image.png`.

Evidence:

| Check | Evidence |
|---|---|
| Training image build | [04-training-image-build.png](evidence/04-training-image-build.png) |
| Serving image build | [05-serving-image-build.png](evidence/05-serving-image-build.png) |
| Mounted container training | [06-container-training.png](evidence/06-container-training.png) |
| Container health and prediction | [07-container-api-validation.png](evidence/07-container-api-validation.png) |

## Kubernetes

- [x] The `docker-desktop` context uses a Ready Kubernetes 1.34.3 node.
- [x] Data and checkpoint PVCs are Bound.
- [x] The training Job completes successfully with 1/1 completions.
- [x] All ten epochs log loss and accuracy as JSON lines.
- [x] The final checkpoint is persisted as `classifier_v1.pt`.
- [x] Final validation accuracy is 0.8777 and best validation loss is 0.3634.
- [x] The serving Deployment has two Ready replicas with zero restarts.
- [x] Liveness/readiness probes and rolling update settings match the assignment.
- [x] The ClusterIP Service maps port 80 to container port 8080.
- [x] Port-forwarded `/health` and `/predict` succeed with the full checkpoint.
- [x] Metrics Server reports node and pod CPU/memory usage.
- [x] HPA targets the serving Deployment at 70% CPU with 2-5 replicas.
- [x] HPA reports `AbleToScale=True` and `ScalingActive=True`.

Evidence:

| Check | Evidence |
|---|---|
| Cluster readiness | [08-kubernetes-cluster-ready.png](evidence/08-kubernetes-cluster-ready.png) |
| Completed training Job | [09-k8s-training-complete.png](evidence/09-k8s-training-complete.png) |
| Two-replica serving rollout | [10-k8s-serving-rollout.png](evidence/10-k8s-serving-rollout.png) |
| Port-forwarded API | [11-k8s-api-validation.png](evidence/11-k8s-api-validation.png) |
| Node and pod metrics | [12-metrics-server-ready.png](evidence/12-metrics-server-ready.png) |
| HPA conditions and limits | [13-hpa-validation.png](evidence/13-hpa-validation.png) |

## Final evidence review

- [x] Screenshots show the relevant commands, results, and namespace.
- [x] No screenshot exposes tokens, credentials, or other secrets.
- [x] Validation statements above describe only observed results.
- [ ] Add the evidence links to the final PR after it is created.
- [ ] Confirm GitHub Actions passes on the final PR.

