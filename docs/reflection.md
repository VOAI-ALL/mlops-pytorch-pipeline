# Reflection

The most challenging part of this assignment was making the same PyTorch
workflow behave consistently across the MLDL environment, Docker, and
Kubernetes. The first full test run on Windows produced six `WinError 5`
permission errors even though nine tests passed. Resolving the temporary-path
handling and rerunning the suite gave me confidence that the failures were
environmental rather than model defects. I then used a one-epoch smoke
configuration before the full run so that configuration loading, metric logging,
early stopping, and checkpoint creation could be checked without repeatedly
waiting for a long training cycle.

Containerization made the separation between training and inference much
clearer. I built independent multi-stage images with pinned dependencies,
mounted the configuration and checkpoint directories, and verified that the
serving image ran as a non-root user. The health endpoint was especially useful
because it distinguished a running web process from a service that had actually
loaded a valid checkpoint. Sending a real image to the prediction endpoint and
receiving all CIFAR-10 class probabilities confirmed that the checkpoint
metadata, preprocessing, model reconstruction, and API contract were
compatible.

Kubernetes introduced the most troubleshooting. During the training Job, the
log initially appeared to stop at 100%, and following logs through the Job
returned after only two epochs. Checking the specific pod showed that training
was still progressing. The completed run reached 87.77% validation accuracy
after ten epochs and persisted `classifier_v1.pt` for the serving Deployment. I
then verified two Ready replicas, rolling deployment behavior, health probes,
the ClusterIP Service, and a successful prediction through port forwarding.

The final issue was resource monitoring on Docker Desktop Kubernetes. Metrics
Server deployed but could not initially become available because of kubelet
certificate validation in the local kind cluster. Applying the narrowly scoped
`--kubelet-insecure-tls` patch allowed node and pod metrics to appear, after
which the HPA reported valid CPU utilization with a 70% target and a two-to-five
replica range. Working in layers (tests, smoke training, containers, the
Kubernetes Job, serving, and autoscaling) made each failure easier to isolate
and produced evidence I could verify at every stage.
