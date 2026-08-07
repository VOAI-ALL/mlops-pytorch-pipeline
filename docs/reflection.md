# Reflection Draft

> Personalize this draft before submission. Keep the final response between 300
> and 500 words and ensure it reflects your own experience.

The most challenging part of this assignment was connecting the training and
serving stages through storage while keeping each environment reproducible. A
model that works in a local Python session is only one part of a production-style
pipeline. The training process also had to accept external configuration, emit
machine-readable metrics, save enough metadata for inference, and write the
checkpoint to a location that Docker and Kubernetes could persist. I addressed
this by keeping paths configurable and storing the architecture, number of
classes, class names, and model state in the same checkpoint.

Containerizing the workloads highlighted the difference between training and
inference dependencies. Separate requirement files and Dockerfiles made the
serving image simpler and prevented development-only packages from being added.
The serving container also runs as a non-root user and exposes a health check,
which required the application to distinguish between a running web server and
a successfully loaded model. Returning an unhealthy response when the checkpoint
is unavailable makes deployment failures visible instead of silently accepting
requests.

Kubernetes introduced the most infrastructure-related reasoning. The training
Job is temporary, but its dataset and output must survive after its pod exits.
PersistentVolumeClaims provide that continuity, and the serving Deployment mounts
the checkpoint claim read-only. I also learned why readiness and liveness probes
serve different purposes: readiness controls whether a pod receives traffic,
whereas liveness allows Kubernetes to restart a broken process. Resource requests
and limits, rolling updates, and the HorizontalPodAutoscaler turn the API into a
more realistic service than simply running a container.

Testing the system in layers was important. Unit tests caught interface problems
without requiring a dataset download. A small smoke configuration then verified
real training and checkpoint creation before the full ten-epoch run. Docker tests
confirmed volume and user behavior, while the final Kubernetes validation checked
the Job, persistent storage, two serving replicas, probes, Service, HPA, and a
port-forwarded prediction. This staged approach made failures easier to isolate
and produced clearer evidence for the final pull request.

