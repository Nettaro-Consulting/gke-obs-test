# Acceso a los Componentes del Stack de Observabilidad

Este documento explica cómo acceder a los diferentes componentes de tu stack de observabilidad desplegado en GKE, que incluye Loki para logs, Tempo para trazas y Grafana para visualización, utilizando acceso directo por IP a través de servicios LoadBalancer.

## 1. Acceso a Loki (Logs)

Loki es tu sistema de agregación de logs.

*   **URL de Ingesta (para aplicaciones):** `http://<LOKI_EXTERNAL_IP>:3100/loki/api/v1/push`
    *   Esta es la URL a la que tu aplicación externa (`send_telemetry.py`) enviará los logs.
    *   Para obtener la IP externa de Loki, ejecuta:
        ```bash
        kubectl get svc loki-stack -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
        ```

*   **Acceso para Consulta (vía Grafana):**
    1.  Abre tu interfaz de Grafana (ver sección 3).
    2.  Asegúrate de que Loki esté configurado como una fuente de datos en Grafana.
    3.  Utiliza el explorador de logs de Grafana para consultar tus logs.

## 2. Acceso a Tempo (Trazas)

Tempo es tu sistema de almacenamiento de trazas distribuidas. La ingesta de trazas se realiza a través de la API OTLP (OpenTelemetry Protocol), y la consulta se realiza a través de Grafana.

*   **URL de Ingesta OTLP (para aplicaciones):**
    *   **HTTP:** `http://<TEMPO_DISTRIBUTOR_EXTERNAL_IP>:4318/v1/traces`
    *   **gRPC:** `http://<TEMPO_DISTRIBUTOR_EXTERNAL_IP>:4317`
    *   Estas son las URLs a las que tu aplicación externa (`send_telemetry.py`) enviará las trazas.
    *   Para obtener la IP externa del distribuidor de Tempo, ejecuta:
        ```bash
        kubectl get svc tempo-distributor -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
        ```

*   **Acceso para Consulta (vía Grafana):**
    1.  Abre tu interfaz de Grafana (ver sección 3).
    2.  Asegúrate de que Tempo esté configurado como una fuente de datos en Grafana.
    3.  Utiliza el explorador de trazas de Grafana para buscar y visualizar tus trazas.

## 3. Acceso a Grafana (Visualización)

Grafana es la interfaz unificada para visualizar tus métricas, logs y trazas.

*   **URL de Acceso:** `http://<GRAFANA_EXTERNAL_IP>:80`
    *   Para obtener la IP externa de Grafana, ejecuta:
        ```bash
        kubectl get svc grafana -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
        ```

*   **Configuración de Fuentes de Datos en Grafana:**
    Para visualizar los datos de Loki y Tempo, debes configurarlos como fuentes de datos en Grafana. Estas configuraciones ya están incluidas en el despliegue de Grafana a través de `datasources.yaml` en el Helm chart, apuntando a los servicios internos del clúster:
    *   **Loki:**
        *   Tipo: Loki
        *   URL: `http://loki-stack.monitoring.svc.cluster.local:3100`
    *   **Tempo:**
        *   Tipo: Tempo
        *   URL: `http://tempo-distributor.monitoring.svc.cluster.local:3200` (o `http://tempo-query-frontend.monitoring.svc.cluster.local:3200` si se usa el query-frontend para consultas)

## Notas Importantes

*   **Acceso Directo por IP:** Todos los componentes ahora son accesibles directamente a través de sus IPs externas asignadas por los servicios `LoadBalancer`.
*   **Sin Seguridad TLS (HTTP):** La comunicación con estos servicios se realiza a través de HTTP sin cifrar. **Esto no es seguro y no se recomienda para entornos de producción.** Es adecuado para entornos de desarrollo o pruebas donde la seguridad no es una preocupación principal.
*   **Credenciales de Grafana:** Si tu instancia de Grafana requiere autenticación, asegúrate de tener las credenciales correctas para acceder.