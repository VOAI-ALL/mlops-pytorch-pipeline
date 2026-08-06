# Validation Evidence

Store genuine screenshots here only while preparing the final pull request. Suggested names:

- `01-unit-tests.png`
- `02-training-image-build.png`
- `03-container-training.png`
- `04-serving-image-build.png`
- `05-container-prediction.png`
- `06-k8s-training-job.png`
- `07-k8s-serving-pods.png`
- `08-k8s-prediction.png`
- `09-hpa-status.png`

The directory is ignored by default to avoid committing unverified or machine-specific evidence. Force-add only the selected final screenshots after reviewing them:

```powershell
git add -f docs/evidence/<approved-file>.png
```

Never create or edit evidence to imply a command succeeded when it did not.

