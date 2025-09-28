#!/bin/bash

NAMESPACE="monitoring"
FILE="statefulsets_replicas.txt"

function sleep_statefulsets() {
    # Vaciar archivo anterior
    > $FILE

    # Guardar nombre y réplicas y escalar a 0
    kubectl get statefulset -n $NAMESPACE -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.spec.replicas}{"\n"}{end}' | while read name replicas; do
        echo "$name $replicas" >> $FILE
        kubectl scale statefulset $name --replicas=0 -n $NAMESPACE
        echo "Dormido: $name (réplicas guardadas: $replicas)"
    done

    echo "Todos los StatefulSets dormidos. Info guardada en $FILE."
}

function wake_statefulsets() {
    if [ ! -f "$FILE" ]; then
        echo "Archivo $FILE no encontrado. No se pueden restaurar réplicas."
        exit 1
    fi

    while read name replicas; do
        kubectl scale statefulset $name --replicas=$replicas -n $NAMESPACE
        echo "Despertado: $name (réplicas restauradas: $replicas)"
    done < $FILE
}

# Validar parámetro
if [ "$1" == "--sleep" ]; then
    sleep_statefulsets
elif [ "$1" == "--wake" ]; then
    wake_statefulsets
else
    echo "Uso: $0 --sleep | --wake"
    exit 1
fi

