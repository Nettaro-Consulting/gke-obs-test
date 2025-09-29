 1 # Mecanismos de Conexión a Servicios del Cluster                                                                         │
 │     2                                                                                                                          │
 │     3 Este documento describe cómo acceder a las interfaces de usuario (UI) de los principales servicios desplegados en este   │
 │       clúster de Kubernetes.                                                                                                   │
 │     4                                                                                                                          │
 │     5 ---                                                                                                                      │
 │     6                                                                                                                          │
 │     7 ## 1. ArgoCD                                                                                                             │
 │     8                                                                                                                          │
 │     9 ArgoCD es la herramienta utilizada para la entrega continua y el despliegue de aplicaciones (GitOps).                    │
 │    10                                                                                                                          │
 │    11 - **Método de Acceso:** IP Externa (LoadBalancer)                                                                        │
 │    12 - **URL:** `https://35.192.74.147`                                                                                       │
 │    13 - **Usuario:** `admin`                                                                                                   │
 │    14 - **Contraseña:** La contraseña inicial se puede obtener con el siguiente comando:                                       │
 │    15   ```bash                                                                                                                │
 │    16   kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d                    │
 │    17   ```                                                                                                                    │
 │    18                                                                                                                          │
 │    19 ---                                                                                                                      │
 │    20                                                                                                                          │
 │    21 ## 2. Grafana                                                                                                            │
 │    22                                                                                                                          │
 │    23 Grafana es la plataforma de visualización para métricas, logs y trazas.                                                  │
 │    24                                                                                                                          │
 │    25 - **Método de Acceso:** `kubectl port-forward`                                                                           │
 │    26 - **Comando (ejecutar en una terminal y dejar corriendo):**                                                              │
 │    27   ```bash                                                                                                                │
 │    28   kubectl port-forward svc/grafana 3000:80 -n monitoring                                                                 │
 │    29   ```                                                                                                                    │
 │    30 - **URL:** `http://localhost:3000`                                                                                       │
 │    31 - **Usuario:** `admin`                                                                                                   │
 │    32 - **Contraseña:** `prom-operator`                                                                                        │
 │    33                                                                                                                          │
 │    34 ---                                                                                                                      │
 │    35                                                                                                                          │
 │    36 ## 3. Prometheus                                                                                                         │
 │    37                                                                                                                          │
 │    38 Prometheus es la base de datos de series temporales para almacenar métricas. Su UI permite ejecutar consultas directas.  │
 │    39                                                                                                                          │
 │    40 - **Método de Acceso:** `kubectl port-forward`                                                                           │
 │    41 - **Comando (ejecutar en una terminal y dejar corriendo):**                                                              │
 │    42   ```bash                                                                                                                │
 │    43   kubectl port-forward svc/prometheus-stack-kube-prom-prometheus 9090:9090 -n monitoring                                 │
 │    44   ```                                                                                                                    │
 │    45 - **URL:** `http://localhost:9090`                                                                                       │
 │    46                                                                                                                          │
 │    47 ---                                                                                                                      │
 │    48                                                                                                                          │
 │    49 ## 4. Jaeger                                                                                                             │
 │    50                                                                                                                          │
 │    51 Jaeger es el sistema de tracing para monitorizar y solucionar problemas en arquitecturas de microservicios.              │
 │    52                                                                                                                          │
 │    53 - **Método de Acceso:** `kubectl port-forward`                                                                           │
 │    54 - **Comando (ejecutar en una terminal y dejar corriendo):**                                                              │
 │    55   ```bash                                                                                                                │
 │    56   kubectl port-forward svc/jaeger-query 16686:80 -n monitoring                                                           │
 │    57   ```                                                                                                                    │
 │    58 - **URL:** `http://localhost:16686`                                                                                      │
 │    59                                                                                                                          │
 │    60 ---                                                                                                                      │
 │    61                                                                                                                          │
 │    62 ## 5. Alertmanager                                                                                                       │
 │    63                                                                                                                          │
 │    64 Alertmanager gestiona las alertas enviadas por Prometheus, encargándose de deduplicarlas, agruparlas y enrutarlas.       │
 │    65                                                                                                                          │
 │    66 - **Método de Acceso:** `kubectl port-forward`                                                                           │
 │    67 - **Comando (ejecutar en una terminal y dejar corriendo):**                                                              │
 │    68   ```bash                                                                                                                │
 │    69   kubectl port-forward svc/prometheus-stack-kube-prom-alertmanager 9093:9093 -n monitoring                               │
 │    70   ```                                                                                                                    │
 │    71 - **URL:** `http://localhost:9093`                                                                                       │
 │    72                                                                                                                          │
 │    73 ---                                                                                                                      │
 │    74                                                                                                                          │
 │    75 **Nota:** Cada comando `port-forward` requiere su propia terminal y debe permanecer en ejecución para mantener el        │
 │       acceso al servicio.                     
