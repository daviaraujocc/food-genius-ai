#!/bin/bash


set -e


install_prometheus() {
    echo "Installing Prometheus Operator..."
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm repo update prometheus-community
    helm install prometheus prometheus-community/kube-prometheus-stack \
        -f ./observability/prometheus-values.yaml \
        --namespace monitoring --create-namespace
    echo "Prometheus Operator installed."
}


install_grafana() {
    echo "Installing Grafana..."
    helm repo add grafana https://grafana.github.io/helm-charts
    helm repo update grafana
    helm install grafana grafana/grafana \
        -f ./observability/grafana-values.yaml \
        --namespace monitoring --create-namespace
    echo "Grafana installed."
}


apply_dependencies() {
    echo "Applying dependencies..."
    kubectl apply -f observability/podmonitor.yaml
    echo "Dependencies applied."
}


main() {
    install_prometheus
    install_grafana
    apply_dependencies
}


main