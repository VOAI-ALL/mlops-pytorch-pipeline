# Submission Checklist

## Repository

- [ ] Public repository is named `mlops-pytorch-pipeline`.
- [ ] All final code is on `main` through pull requests.
- [ ] At least four feature PRs are merged: two labeled Week 1 and two Week 2.
- [ ] Commit messages follow Conventional Commits.
- [ ] CI passes on the final PR.
- [ ] No secrets, datasets, checkpoints, or assignment PDF are committed.

## Required implementation

- [ ] Required project files and directories are present.
- [ ] ResNet-18 trains on CIFAR-10 and saves the best checkpoint.
- [ ] Training reads YAML from a mounted path or `CONFIG_PATH`.
- [ ] Metrics are emitted as JSON lines and early stopping is supported.
- [ ] `/health` and `/predict` satisfy the API contract.
- [ ] Training and serving Docker images meet all assignment constraints.
- [ ] Kubernetes Job, storage, Deployment, Service, probes, resources, rolling
  update, and HPA have been validated.

## Evidence and course platform

- [ ] Final PR contains terminal output or screenshots for every required step.
- [ ] Full prediction response is visible in the evidence.
- [ ] Reflection has been personalized and contains 300–500 words.
- [ ] Submit the public GitHub repository URL.
- [ ] Submit the final validation PR URL.
- [ ] Submit the final reflection.
