# Pull Request Description Drafts

These drafts must be checked against the actual PR diff and CI result before use.
Obtain approval before creating each PR.

## PR 1 - Project foundation (Week 1)

**Title:** `task: establish ML project foundation`

### Summary

- Add the project structure, pinned dependency files, YAML training
  configurations, and Python project metadata.
- Add documentation scaffolding for validation evidence and submission review.

### Validation

- Dependency versions are pinned and both YAML configurations parse successfully.
- Final end-to-end evidence is indexed in `docs/validation.md`.

## PR 2 - PyTorch pipeline (Week 1)

**Title:** `feat: implement CIFAR-10 training and inference`

### Summary

- Add a CIFAR-adapted ResNet-18 and CIFAR-10 data loaders.
- Add configurable training, JSON metrics, early stopping, and checkpointing.
- Add FastAPI health/prediction endpoints and automated tests.

### Validation

- Final local suite: 16 tests passed.
- Smoke training emitted JSON metrics and saved `classifier_smoke.pt`.
- Local health and prediction endpoints returned successful responses.

## PR 3 - Docker containerization (Week 2)

**Title:** `feat: containerize training and model serving`

### Summary

- Add separate multi-stage training and serving images.
- Run model serving as a non-root user with a health check.
- Add Docker build/test CI and exclude unnecessary files from image build contexts.

### Validation

- Both Linux/AMD64 images built successfully.
- Mounted training persisted its checkpoint to the host.
- Serving ran as user `app`, became healthy, and returned a prediction.

## PR 4 - Kubernetes deployment (Week 2)

**Title:** `feat: orchestrate training and serving on Kubernetes`

### Summary

- Add the namespace, ConfigMap, PVC-backed training Job, serving Deployment,
  Service, probes, rolling strategy, resources, and HPA.
- Add infrastructure tests, the Docker Desktop Metrics Server patch, and
  verified end-to-end validation evidence.

### Validation

- The training Job completed all ten epochs and persisted `classifier_v1.pt`.
- Two serving replicas rolled out and passed health/prediction checks.
- Metrics Server and the 2-5 replica HPA reported valid CPU metrics.

## Final PR - Develop to main

**Title:** `release: validate end-to-end ML pipeline`

### Summary

- Release the tested training and serving pipeline.
- Provide final Docker and Kubernetes validation evidence.

### Validation evidence

- Local tests: 16 passed; see `docs/evidence/01-unit-tests.png`.
- Docker training and serving: see evidence 04-07 in `docs/evidence/`.
- Kubernetes Job and checkpoint: 10 epochs, 87.77% validation accuracy; see evidence 09.
- Kubernetes serving and prediction: two Ready replicas and successful API; see evidence 10-11.
- Autoscaling: valid node/pod metrics and active 2-5 replica HPA; see evidence 12-13.

### Submission review

- [ ] All four feature PRs are merged.
- [ ] All screenshots/logs are genuine and readable.
- [ ] README architecture and setup instructions are current.
- [ ] Reflection is personalized and 300–500 words.
