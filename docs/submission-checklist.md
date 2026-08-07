# Submission Checklist

## Repository

- [x] Public repository is named `mlops-pytorch-pipeline`.
- [ ] All final code is on `main` through pull requests.
- [x] At least four feature PRs are merged: two covering Week 1 and two covering
  Week 2.
- [x] Commit messages follow Conventional Commits.
- [ ] CI passes on the final PR.
- [x] No secrets, datasets, checkpoints, or assignment PDF are committed.

## Required implementation

- [x] Required project files and directories are present.
- [x] ResNet-18 trains on CIFAR-10 and saves the best checkpoint.
- [x] Training reads YAML from a mounted path or `CONFIG_PATH`.
- [x] Metrics are emitted as JSON lines and early stopping is supported.
- [x] `/health` and `/predict` satisfy the API contract.
- [x] Training and serving Docker images meet all assignment constraints.
- [x] Kubernetes Job, storage, Deployment, Service, probes, resources, rolling
  update, and HPA have been validated.

## Evidence and course platform

- [ ] Final PR contains terminal output or screenshots for every required step.
- [x] Full prediction response is visible in the evidence.
- [x] Reflection has been personalized and contains 300-500 words.
- [ ] Submit the public GitHub repository URL.
- [ ] Submit the final validation PR URL.
- [ ] Submit the final reflection.
