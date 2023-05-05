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

## References
- [Flink Kubernetes Operator](https://github.com/apache/flink-kubernetes-operator)
