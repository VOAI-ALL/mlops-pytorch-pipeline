# Validation Evidence

This directory contains genuine screenshots captured during local, Docker, and
Kubernetes validation.

| File | Demonstrates |
|---|---|
| `01-unit-tests.png` | Final test suite: 16 passed |
| `02-local-smoke-training.png` | Local JSON metrics and smoke checkpoint |
| `03-local-api-validation.png` | Local health and prediction endpoints |
| `04-training-image-build.png` | Successful training image build |
| `05-serving-image-build.png` | Successful serving image build |
| `06-container-training.png` | Mounted container training and checkpoint |
| `07-container-api-validation.png` | Non-root user, Docker health, and prediction |
| `08-kubernetes-cluster-ready.png` | Ready Docker Desktop Kubernetes node |
| `09-k8s-training-complete.png` | Ten epochs, final checkpoint, and completion |
| `10-k8s-serving-rollout.png` | Successful rollout and two Ready replicas |
| `11-k8s-api-validation.png` | Port-forwarded health and prediction |
| `12-metrics-server-ready.png` | Node and serving-pod resource metrics |
| `13-hpa-validation.png` | HPA CPU target, replica limits, and conditions |

The screenshots were reviewed for readability and accidental credential or
secret exposure before inclusion. They may show local filesystem paths and
non-sensitive local environment names as part of the terminal context.

