- [Overview](#overview)
- [Create local Kubernetes cluster](#create-local-kubernetes-cluster)
- [Create Flink cluster.](#create-flink-cluster)
- [Install pre-requisites components](#install-pre-requisites-components)
- [References](#references)

# PyFlink Playground
Explore PyFlink with ease using this Helm chart-based playground.

## Overview
This project is designed not only for deploying simple examples but also for handling complex stream processing scenarios integrated with various storage services like Kafka, S3, and more.

With Kubernetes and Helm chart, you can effortlessly deploy complex infrastructures on your local machine. Let's put elephants to the refrigerator 🚀

## Create local Kubernetes cluster
First, let's create a Kubernetes cluster on your local machine. We'll use [K3D](https://k3d.io/v5.4.9/#installation) to set up the local cluster. Make sure you have downloaded it before running the command below.

```shell
$ k3d cluster create local-cluster \
    --api-port 6550 \
    -p "30000-30010:30000-30010@server:0" \
    --agents 2
```

- `-p 30000-30010:30000-30010` : This binds the local port to the cluster, allowing you to access the Flink dashboard locally.

```
💡 Do not allocate large port ranges `-p 30000-30010:30000-30010`, 
Docker creates proxy process for every port bounded, 
it makes your computer super slow.
```

## Create Flink cluster.
```shell
# Insall Flink Kubernetes Operator
helm repo add flink-operator-repo \
    https://downloads.apache.org/flink/flink-kubernetes-operator-1.4.0/
helm install -f flink/values.yml \
    flink-kubernetes-operator \
    flink-operator-repo/flink-kubernetes-operator

# Deploy Flink Server
kubectl apply -f flink/deployment.yml
```

## Install pre-requisites components
The example code uses external storages for both `source` and `sink`. You can easily install these components using the Helm chart.

```shell
$ helm install play ./helm-charts
💡 Make sure to name it as `play`.
```

Verify that these components are successfully installed using kubectl.

```shell
$ kubectl get pods
NAME                                         READY   STATUS    RESTARTS   AGE
flink-kubernetes-operator-545c768689-m8kpv   1/1     Running   0          11m
play-minio-78fd77d9cd-zw7qh                  0/1     Pending   0          2m21s
play-minio-post-job-crwz7                    1/1     Running   0          2m21s
play-kafka-faker-68bc96b949-9xrth            1/1     Running   0          2m21s
play-kafka-0                                 1/1     Running   0          2m21s
play-kafka-ui-6d464f9fd-4mg5w                1/1     Running   0          2m21s
```

## Install Flink, Java and Python
This is the trickiest part. You need to manually install the Flink binary and ensure that the versions of the following components match: [Here is a guide for installing Flink](https://nightlies.apache.org/flink/flink-docs-stable/docs/try-flink/local_installation/)

- Python 3.9
- Java 11
- Flink 1.17.0

If you wish to change the version of Flink, you can manually modify it from Helm chart of this project. 

```shell
$ flink --version
Version: 1.17.0, Commit ID: 69ecda0
```

## Deploy FLink Job
Congratulations! You've reached the final step. Now you're ready to deploy your first Flink job.

```shell
flink run -py ../jobs/helloworld/main.py -m localhost:30000
```

To see what the job is doing. Visit to Flink Dashboard[localhost:30000](localhost:30000)

## References
- [Flink Kubernetes Operator](https://github.com/apache/flink-kubernetes-operator)
- [Flink : Python API](https://nightlies.apache.org/flink/flink-docs-release-1.17/docs/dev/python/overview/)