- [Overview](#overview)
- [Create local Kubernetes cluster](#create-local-kubernetes-cluster)
- [Create Flink cluster.](#create-flink-cluster)
- [Install pre-requisites components](#install-pre-requisites-components)
- [References](#references)

# PyFlink Playground
A playground for PyFlink written with Helm chart.

## Overview
This project is not only for deploying simple example but also complex stream processing integrated with various storage services such as Kafka, S3 and etc.

Kuberentes with helm chart helps us to deploy complex infrastructure within local machine with ease. Let's put elephants to the refrigerator 🚀

## Create local Kubernetes cluster
First of all, let's create a kubernetes cluster in local. To configure local cluster we're going to use [K3D](https://k3d.io/v5.4.9/#installation). Before you run belo command, make sure that you downloaded it first.

```shell
$ k3d cluster create local-cluster \
    --api-port 6550 \
    -p "30000-30010:30000-30010@server:0" \
    --agents 2
```

- `-p 30000-30010:30000-30010` : This bound the local port to the cluster, It helps us to visit the Flink dashboard in local.

```
💡 Do not allocate large port ranges `-p 30000-30010:30000-30010`, 
Docker creates proxy process for every port bounded, 
it makes your computer super slow.
```

## Create Flink cluster.
```shell
helm repo add flink-operator-repo \
    https://downloads.apache.org/flink/flink-kubernetes-operator-1.4.0/
helm install -f flink/values.yml \
    flink-kubernetes-operator \
    flink-operator-repo/flink-kubernetes-operator
```

## Install pre-requisites components
The example code uses Kafka as messages and MinIO as storage. You can simply install these components by Helm chart.

```shell
$ helm install play ./helm-charts
```

```
💡 Until now, you need to name it as `play`.
```

Kubectl show you that these components is successfully installed.

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
This is the most hard part here. you need to install flink binary manually and make sure that the version of thoese is same as below.

- Python 3.9
- Java 11
- Flink 1.17.0

If you want to change the version of Flink, you can manually modify it from helm chart in this project. [This shows how to install Flink](https://nightlies.apache.org/flink/flink-docs-stable/docs/try-flink/local_installation/)

```shell
$ flink --version
Version: 1.17.0, Commit ID: 69ecda0
```

## Deploh FLink Job
All Done!, If you follow the description to this line. You're now ready to deploy your first flink job.

```shell
flink run -py ../jobs/basic/job.py -m localhost:30000
```

Let's check what it does in Flink dashboard. Please visit [localhost:30000](localhost:30000)

## References
- [Flink Kubernetes Operator](https://github.com/apache/flink-kubernetes-operator)
- [Flink : Python API](https://nightlies.apache.org/flink/flink-docs-release-1.17/docs/dev/python/overview/)