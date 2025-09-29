# Deployment de Stack de Observabilidad con Argo CD y Envío de Telemetría

Este `README.md` detalla cómo desplegar el stack de observabilidad (Loki, Tempo y Grafana) en un clúster de GKE utilizando Argo CD con el patrón "apps of apps", y cómo enviar telemetría (logs y trazas) a estos servicios a través de servicios LoadBalancer.

## 1. Estructura del Repositorio

El repositorio está organizado para facilitar el despliegue con Argo CD utilizando el patrón "apps of apps":

```
.exported-apps/
├── argocd-apps/
│   ├── all-observability-apps.yaml       # Aplicación padre de Argo CD (apps of apps)
│   ├── grafana.yaml                      # Aplicación Argo CD para Grafana
│   ├── jaeger-operator.yaml              # Aplicación Argo CD para Jaeger Operator
│   ├── loki-stack.yaml                   # Aplicación Argo CD para Loki
│   └── tempo.yaml                        # Aplicación Argo CD para Tempo
├── requirements.txt                      # Dependencias de la aplicación Python
├── send_telemetry.py                     # Aplicación Python para enviar telemetría
└── README.md                             # Este archivo
```

## 2. Deployment del Stack de Observabilidad con Argo CD

### Prerrequisitos

Antes de proceder, asegúrate de tener lo siguiente en tu clúster de GKE:

*   **Argo CD:** Instalado y configurado.

### Pasos de Deployment

1.  **Clona este repositorio** en tu máquina local.

2.  **Aplica la aplicación padre de Argo CD** a tu clúster. Esta aplicación se encargará de desplegar todas las aplicaciones hijas definidas en el directorio `argocd-apps/`.

    ```bash
    kubectl apply -f argocd-apps/all-observability-apps.yaml
    ```

3.  **Verifica en la UI de Argo CD:** Accede a la interfaz de usuario de Argo CD. Deberías ver la aplicación `all-observability-apps` y, dentro de ella, las aplicaciones hijas (`grafana`, `loki-stack`, `jaeger-operator`, `tempo`). Asegúrate de que todas se sincronicen y estén `Healthy`.

### Configuración Post-Deployment

Los servicios de Grafana, Loki y Tempo se exponen a través de servicios `LoadBalancer`, lo que les asignará una IP externa a cada uno.

1.  **Obtener IPs Externas:**
    *   **Grafana:**
        ```bash
        kubectl get svc grafana -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
        ```
    *   **Loki:**
        ```bash
        kubectl get svc loki-stack -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
        ```
    *   **Tempo (Distributor):**
        ```bash
        kubectl get svc tempo-distributor -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
        ```

## 3. Envío de Telemetría

Una vez que el stack de observabilidad esté desplegado y accesible, puedes usar la aplicación Python `send_telemetry.py` para enviar logs y trazas de ejemplo.

### 1. Dependencias

Las dependencias necesarias están listadas en `requirements.txt`:

```
python-loki
opentelemetry-sdk
opentelemetry-exporter-otlp-proto-http
```

### 2. Pasos para Enviar Telemetría

1.  **Navega al directorio del proyecto** (donde se encuentran `send_telemetry.py` y `requirements.txt`):
    ```bash
    cd /ruta/a/tu/repositorio
    ```
2.  **Instala las dependencias de Python:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Ejecuta el script:**
    ```bash
    # Reemplaza <LOKI_EXTERNAL_IP> y <TEMPO_DISTRIBUTOR_EXTERNAL_IP> con las IPs obtenidas
    LOKI_URL="http://<LOKI_EXTERNAL_IP>:3100/loki/api/v1/push" \
    TEMPO_OTLP_HTTP_ENDPOINT="http://<TEMPO_DISTRIBUTOR_EXTERNAL_IP>:4318/v1/traces" \
    python send_telemetry.py
    ```

    El script enviará logs y trazas a las IPs externas de Loki y Tempo.

## 4. Verificación de Datos

Una vez que la aplicación Python se haya ejecutado, podrás verificar los logs y trazas en tu interfaz de Grafana.

*   **Acceso a Grafana:** Abre tu navegador y ve a `http://<GRAFANA_EXTERNAL_IP>:80` (reemplaza con la IP obtenida).
*   **Logs en Loki:** En Grafana, busca logs con la etiqueta `application=my-external-app`.
*   **Trazas en Tempo:** En Grafana, busca trazas generadas por el servicio `my-external-app`.

## Notas Importantes

*   **Sin Seguridad TLS (HTTP):** La comunicación con estos servicios se realiza a través de HTTP sin cifrar. **Esto no es seguro y no se recomienda para entornos de producción.** Es adecuado para entornos de desarrollo o pruebas donde la seguridad no es una preocupación principal.
*   **Credenciales de Grafana:** Si tu instancia de Grafana requiere autenticación, asegúrate de tener las credenciales correctas para acceder.
