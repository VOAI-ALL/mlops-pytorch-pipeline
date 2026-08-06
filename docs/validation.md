# End-to-End Validation Record

Complete this record with real command output and screenshots. Do not mark an
item complete until the command has succeeded on the submission environment.

## Environment

- [ ] `conda activate MLDL`
- [ ] `python --version` shows Python 3.10+
- [ ] `python -c "import torch; print(torch.__version__, torch.cuda.is_available())"`
- [ ] `docker --version`
- [ ] `kubectl version --client`

## Local application

- [ ] `python -m pytest -q` passes every test.
- [ ] Smoke training emits JSON metrics.
- [ ] `classifier_smoke.pt` is created.
- [ ] Local `/health` returns HTTP 200 with the checkpoint loaded.
- [ ] Local `/predict` returns ten probabilities summing approximately to one.

## Docker

- [ ] `mlops-train:v1` builds successfully.
- [ ] Mounted container training creates a host checkpoint.
- [ ] `mlops-serve:v1` builds successfully.
- [ ] Serving container reports user `app` and health `healthy`.
- [ ] Container `/predict` succeeds with `test_image.png`.

Evidence:

| Check | Screenshot or pasted output |
|---|---|
| Training image build | TODO |
| Container training | TODO |
| Serving image build | TODO |
| Container health/prediction | TODO |

## Kubernetes

- [ ] Context is `docker-desktop` and the node is Ready.
- [ ] Both PVCs are Bound.
- [ ] Training Job completes successfully.
- [ ] Training logs contain `checkpoint_saved` and `training_complete`.
- [ ] Deployment has two Ready replicas.
- [ ] Liveness/readiness probes and rolling strategy match the assignment.
- [ ] Service maps port 80 to target port 8080.
- [ ] HPA targets the serving Deployment with 2–5 replicas.
- [ ] Port-forwarded `/health` and `/predict` succeed.

Evidence:

| Check | Screenshot or pasted output |
|---|---|
| Job and logs | TODO |
| Pods and deployment | TODO |
| Service and HPA | TODO |
| Port-forwarded prediction | TODO |

## Final evidence review

- [ ] Screenshots show the relevant commands, results, and namespace.
- [ ] No screenshot exposes tokens, usernames that should remain private, or secrets.
- [ ] PR descriptions describe only results that actually occurred.
- [ ] Final PR contains or links all required validation evidence.

