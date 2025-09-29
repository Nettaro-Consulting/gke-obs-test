# Deployment de Stack de Observabilidad con Argo CD y Envío de Telemetría

Este `README.md` detalla cómo desplegar el stack de observabilidad (Loki y Tempo) en un clúster de GKE utilizando Argo CD con el patrón "apps of apps", y cómo enviar telemetría (logs y trazas) a estos servicios.

## 1. Estructura del Repositorio

El repositorio está organizado para facilitar el despliegue con Argo CD utilizando el patrón "apps of apps":

```
.exported-apps/
├── argocd-apps/
│   ├── all-observability-apps.yaml       # Aplicación padre de Argo CD (apps of apps)
│   ├── jaeger-operator.yaml              # Aplicación Argo CD para Jaeger Operator
│   ├── loki-stack.yaml                   # Aplicación Argo CD para Loki
│   ├── observability-ingresses-app.yaml  # Aplicación Argo CD para los Ingresses
│   ├── tempo.yaml                        # Aplicación Argo CD para Tempo
│   └── ingresses/                        # Directorio con los manifiestos de Ingress
│       ├── loki-ingress.yaml
│       └── tempo-ingress.yaml
├── requirements.txt                      # Dependencias de la aplicación Python
├── send_telemetry.py                     # Aplicación Python para enviar telemetría
└── README.md                             # Este archivo
```

## 2. Deployment del Stack de Observabilidad con Argo CD

### Prerrequisitos

Antes de proceder, asegúrate de tener lo siguiente en tu clúster de GKE:

*   **Argo CD:** Instalado y configurado.
*   **Nginx Ingress Controller:** Instalado y funcionando. Si no lo tienes, puedes instalarlo con Helm:
    ```bash
    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    helm repo update
    helm install ingress-nginx ingress-nginx/ingress-nginx --create-namespace --namespace ingress-nginx
    ```
*   **cert-manager:** Instalado y configurado, con un `Issuer` o `ClusterIssuer` llamado `selfsigned-issuer` (o el nombre que hayas configurado) en el namespace `monitoring`.

### Pasos de Deployment

1.  **Clona este repositorio** en tu máquina local.

2.  **Aplica la aplicación padre de Argo CD** a tu clúster. Esta aplicación se encargará de desplegar todas las aplicaciones hijas definidas en el directorio `argocd-apps/`.

    ```bash
    kubectl apply -f argocd-apps/all-observability-apps.yaml
    ```

3.  **Verifica en la UI de Argo CD:** Accede a la interfaz de usuario de Argo CD. Deberías ver la aplicación `all-observability-apps` y, dentro de ella, las aplicaciones hijas (`loki-stack`, `jaeger-operator`, `tempo`, `observability-ingresses`). Asegúrate de que todas se sincronicen y estén `Healthy`.

### Configuración Post-Deployment

1.  **Configuración de DNS:**
    Debes configurar los registros DNS para los siguientes dominios, apuntándolos a la **dirección IP externa de tu Nginx Ingress Controller**:

    *   `loki.nettaro.com`
    *   `tempo.nettaro.com`

    Puedes obtener la IP externa de tu Ingress Controller con:
    ```bash
    kubectl get svc -n ingress-nginx ingress-nginx-controller -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
    ```

2.  **Verificación de Certificados TLS:**
    `cert-manager` se encarga de emitir los certificados TLS para los dominios configurados. Puedes verificar su estado con:
    ```bash
    kubectl get certificate -n monitoring
    ```
    Asegúrate de que ambos certificados (`loki-tls` y `tempo-tls`) muestren `READY: True`.

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
    python send_telemetry.py
    ```

    El script enviará logs a `https://loki.nettaro.com/loki/api/v1/push` y trazas OTLP (HTTP) a `https://tempo.nettaro.com/v1/traces`.

    Puedes sobrescribir estas URLs mediante las variables de entorno `LOKI_URL` y `TEMPO_OTLP_HTTP_ENDPOINT` respectivamente, por ejemplo:
    ```bash
    LOKI_URL="https://my-custom-loki.com/loki/api/v1/push" TEMPO_OTLP_HTTP_ENDPOINT="https://my-custom-tempo.com/v1/traces" python send_telemetry.py
    ```

## 4. Verificación de Datos

Una vez que la aplicación Python se haya ejecutado, podrás verificar los logs y trazas en tu interfaz de Grafana, configurada para usar Loki y Tempo como fuentes de datos.

*   **Logs en Loki:** Busca logs con la etiqueta `application=my-external-app`.
*   **Trazas en Tempo:** Busca trazas generadas por el servicio `my-external-app`.