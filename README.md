# GKE Observability Test - Generación y Envío de Telemetría

Este proyecto demuestra cómo generar y enviar logs a Loki y trazas a Tempo desde una aplicación externa a un clúster de GKE, utilizando Nginx Ingress Controller y cert-manager para la exposición externa y la seguridad.

## Componentes de Observabilidad

*   **Loki:** Sistema de agregación de logs de Grafana.
*   **Tempo:** Sistema de almacenamiento de trazas distribuidas de Grafana.
*   **Nginx Ingress Controller:** Gestiona el acceso externo a los servicios del clúster.
*   **cert-manager:** Automatiza la gestión de certificados TLS.

## Configuración de Kubernetes

Para que la aplicación externa pueda comunicarse con Loki y Tempo, hemos configurado Ingresses para exponer estos servicios de forma segura.

### 1. Instalación del Nginx Ingress Controller

Si aún no lo tienes instalado, el Nginx Ingress Controller es necesario. Se instaló usando Helm con los siguientes comandos:

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install ingress-nginx ingress-nginx/ingress-nginx --create-namespace --namespace ingress-nginx
```

### 2. Configuración de Ingress para Loki y Tempo

Se han creado dos recursos Ingress para exponer Loki y Tempo:

*   **`loki-ingress.yaml`**: Expone Loki en `https://loki.nettaro.com`.
*   **`tempo-ingress.yaml`**: Expone Tempo en `https://tempo.nettaro.com` para la ingesta de trazas OTLP (HTTP y gRPC).

Estos archivos se aplicaron al clúster:

```bash
kubectl apply -f loki-ingress.yaml
kubectl apply -f tempo-ingress.yaml
```

### 3. Configuración de Argo CD para Tempo

El archivo `tempo.yaml` (aplicación de Argo CD) fue modificado para incluir un archivo de valores personalizado (`tempo-custom-values.yaml`) que habilita el componente `gateway` de Tempo y su Ingress.

**Es crucial que la aplicación `tempo` en Argo CD se sincronice correctamente** para que estos cambios se apliquen en el clúster.

### 4. Configuración de DNS

Debes configurar los registros DNS para los siguientes dominios, apuntándolos a la **dirección IP externa de tu Nginx Ingress Controller**:

*   `loki.nettaro.com`
*   `tempo.nettaro.com`

Puedes obtener la IP externa de tu Ingress Controller con:

```bash
kubectl get svc -n ingress-nginx ingress-nginx-controller -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

### 5. Verificación de Certificados TLS

`cert-manager` se encarga de emitir los certificados TLS para `loki.nettaro.com` y `tempo.nettaro.com` utilizando el `selfsigned-issuer`. Puedes verificar el estado de los certificados con:

```bash
kubectl get certificate -n monitoring
```

Asegúrate de que ambos certificados (`loki-tls` y `tempo-tls`) muestren `READY: True`.

## Aplicación de Telemetría (Python)

Hemos creado una pequeña aplicación en Python (`send_telemetry.py`) para demostrar el envío de logs y trazas.

### 1. Dependencias

Las dependencias necesarias están listadas en `requirements.txt`:

```
python-loki
opentelemetry-sdk
opentelemetry-exporter-otlp-proto-http
```

### 2. Ejecución de la Aplicación

1.  **Navega al directorio del proyecto:**
    ```bash
    cd /Users/rubencarrasco/exported-apps
    ```
2.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Ejecuta el script:**
    ```bash
    python send_telemetry.py
    ```

El script enviará logs a `https://loki.nettaro.com/loki/api/v1/push` y trazas OTLP (HTTP) a `https://tempo.nettaro.com/v1/traces`. Estas URLs se pueden sobrescribir mediante las variables de entorno `LOKI_URL` y `TEMPO_OTLP_HTTP_ENDPOINT` respectivamente.

## Verificación de Datos

Una vez que la aplicación Python se haya ejecutado, podrás verificar los logs y trazas en tu interfaz de Grafana, configurada para usar Loki y Tempo como fuentes de datos.

*   **Logs en Loki:** Busca logs con la etiqueta `application=my-external-app`.
*   **Trazas en Tempo:** Busca trazas generadas por el servicio `my-external-app`.

   1. Configured Ingress resources for Loki and Tempo, exposing them via loki.nettaro.com and tempo.nettaro.com respectively, with TLS certificates managed
      by cert-manager.
   2. Created a Python application (send_telemetry.py) that sends sample logs to Loki and traces to Tempo using OpenTelemetry.
   3. Created a README.md file with detailed instructions on how to set up the Kubernetes configurations, run the Python application, and verify the
      telemetry data.
   4. Pushed all the changes to your Git repository https://github.com/Nettaro-Consulting/gke-obs-test.git.
