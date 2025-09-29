# Acceso a los Componentes del Stack de Observabilidad

Este documento explica cómo acceder a los diferentes componentes de tu stack de observabilidad desplegado en GKE, que incluye Loki para logs, Tempo para trazas y Grafana para visualización.

## 1. Acceso a Loki (Logs)

Loki es tu sistema de agregación de logs. Aunque Loki tiene una API para ingesta, la forma principal de interactuar y consultar tus logs es a través de Grafana.

*   **URL de Ingesta (para aplicaciones):** `https://loki.nettaro.com/loki/api/v1/push`
    *   Esta es la URL a la que tu aplicación externa (`send_telemetry.py`) envía los logs.

*   **Acceso para Consulta (vía Grafana):**
    1.  Abre tu interfaz de Grafana (por ejemplo, `https://grafana.nettaro.com`).
    2.  Asegúrate de que Loki esté configurado como una fuente de datos en Grafana.
    3.  Utiliza el explorador de logs de Grafana para consultar tus logs.

## 2. Acceso a Tempo (Trazas)

Tempo es tu sistema de almacenamiento de trazas distribuidas. La ingesta de trazas se realiza a través de la API OTLP (OpenTelemetry Protocol), y la consulta se realiza a través de Grafana.

*   **URL de Ingesta OTLP (para aplicaciones):** `https://tempo.nettaro.com/v1/traces`
    *   Esta es la URL a la que tu aplicación externa (`send_telemetry.py`) envía las trazas OTLP (HTTP).
    *   Para gRPC, el endpoint es `https://tempo.nettaro.com:4317` (aunque el Ingress lo maneja en el mismo host).

*   **Acceso para Consulta (vía Grafana):**
    1.  Abre tu interfaz de Grafana (por ejemplo, `https://grafana.nettaro.com`).
    2.  Asegúrate de que Tempo esté configurado como una fuente de datos en Grafana.
    3.  Utiliza el explorador de trazas de Grafana para buscar y visualizar tus trazas.

## 3. Acceso a Grafana (Visualización)

Grafana es la interfaz unificada para visualizar tus métricas, logs y trazas.

*   **URL de Acceso:** `https://grafana.nettaro.com`

*   **Configuración de Fuentes de Datos en Grafana:**
    Para visualizar los datos de Loki y Tempo, debes configurarlos como fuentes de datos en Grafana. Estas configuraciones ya están incluidas en el despliegue de Grafana a través de `datasources.yaml` en el Helm chart, apuntando a los servicios internos del clúster:
    *   **Loki:**
        *   Tipo: Loki
        *   URL: `http://loki-stack.monitoring.svc.cluster.local:3100`
    *   **Tempo:**
        *   Tipo: Tempo
        *   URL: `http://tempo-distributor.monitoring.svc.cluster.local:3200` (o `http://tempo-query-frontend.monitoring.svc.cluster.local:3200` si se usa el query-frontend para consultas)

    **Nota:** La URL para Tempo en la configuración de Grafana debería apuntar al `tempo-distributor` para la ingesta o al `tempo-query-frontend` para la consulta. El `tempo-distributor` es el que recibe las trazas, y el `tempo-query-frontend` es el que se usa para consultar. En la configuración actual del `grafana.yaml`, apunta al `tempo-distributor`.

## Notas Importantes

*   **Configuración de DNS:** Asegúrate de que los registros DNS para `loki.nettaro.com`, `tempo.nettaro.com` y `grafana.nettaro.com` (si aplica) apunten a la IP externa de tu Nginx Ingress Controller.
*   **Certificados TLS:** Los certificados para `loki.nettaro.com` y `tempo.nettaro.com` son gestionados por `cert-manager` utilizando un `selfsigned-issuer`. Esto significa que tu navegador podría mostrar una advertencia de seguridad al acceder a estas URLs directamente, ya que el certificado no está firmado por una autoridad de confianza pública. Para producción, se recomienda usar un `ClusterIssuer` como Let's Encrypt.
*   **Credenciales de Grafana:** Si tu instancia de Grafana requiere autenticación, asegúrate de tener las credenciales correctas para acceder.
