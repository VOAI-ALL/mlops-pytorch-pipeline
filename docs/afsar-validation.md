\# Assignment 2 Validation



\## Student Validation



This document records validation performed for Assignment 2.



\### Local FastAPI Validation



The PyTorch model was served using FastAPI and tested using the `/predict`

endpoint with `test\_image.png`.



The API successfully returned a predicted class and probability distribution.



\### Docker Validation



Docker training and serving images will be built and validated as part of

the containerization stage.



\### Kubernetes Validation



The Kubernetes training Job, serving Deployment, Service, and HPA will be

validated using Docker Desktop Kubernetes.

