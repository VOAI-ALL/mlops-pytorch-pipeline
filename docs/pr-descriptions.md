# Pull Request Description Drafts

These drafts must be checked against the actual diff and test results before use.
Replace every `TODO` and obtain approval before creating a PR.

## PR 1 - Project foundation (Week 1)

**Title:** `chore: establish ML project foundation`

### Summary

- Add the required repository structure, pinned dependency files, configuration,
  ignore rules, and GitHub Actions workflow.
- Add documentation scaffolding for validation evidence and submission review.

### Validation

- `TODO: exact commands and real results`

## PR 2 - PyTorch pipeline (Week 1)

**Title:** `feat: implement CIFAR-10 training and inference`

### Summary

- Add a CIFAR-adapted ResNet-18 and CIFAR-10 data loaders.
- Add configurable training, JSON metrics, early stopping, and checkpointing.
- Add FastAPI health/prediction endpoints and automated tests.

### Validation

- `TODO: exact pytest and smoke-training results`

## PR 3 - Docker containerization (Week 2)

**Title:** `feat: containerize training and model serving`

### Summary

- Add separate multi-stage training and serving images.
- Run model serving as a non-root user with a health check.
- Document mounted training, checkpoint persistence, and endpoint verification.

### Validation

- `TODO: exact image builds, container logs, and screenshot links`

## PR 4 - Kubernetes deployment (Week 2)

**Title:** `feat: orchestrate training and serving on Kubernetes`

### Summary

- Add the namespace, ConfigMap, PVC-backed training Job, serving Deployment,
  Service, probes, rolling strategy, resources, and HPA.
- Add the Docker Desktop Kubernetes validation workflow.

### Validation

- `TODO: exact kubectl results and screenshot links`

## Final PR - Develop to main

**Title:** `release: validate end-to-end ML pipeline`

### Summary

- Release the tested training and serving pipeline.
- Provide final Docker and Kubernetes validation evidence.

### Validation evidence

- Local tests: `TODO`
- Docker training and serving: `TODO`
- Kubernetes Job and checkpoint: `TODO`
- Kubernetes serving and prediction: `TODO`

### Submission review

- [ ] All four feature PRs are merged.
- [ ] All screenshots/logs are genuine and readable.
- [ ] README architecture and setup instructions are current.
- [ ] Reflection is personalized and 300–500 words.
