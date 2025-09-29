
# 📊 GKE Observability Stack (ArgoCD)

Este repositorio contiene los manifiestos exportados de las aplicaciones de **observabilidad** desplegadas en un clúster de **Google Kubernetes Engine (GKE)** y gestionadas con **ArgoCD**.

Incluye:
- **Prometheus/Grafana** → Métricas y visualización
- **Jaeger** → Trazas distribuidas
- **Tempo** → Backend de trazas (compatible con Jaeger/OTel)
- **Mimir** → Almacenamiento de métricas a largo plazo
- **Loki** → Logs centralizados
- **cert-manager** → Certificados TLS

---

## 🌐 Acceso a los Servicios

Todos los servicios están desplegados en el **namespace `monitoring`**  
Para acceso local:

```bash
kubectl port-forward -n monitoring svc/<servicio> <puerto_local>:<puerto_servicio>
````

| Componente  | Puerto Local | Descripción                        | Ejemplo de acceso               |
| ----------- | ------------ | ---------------------------------- | ------------------------------- |
| **ArgoCD**  | `8080`       | Gestión de aplicaciones            | `http://localhost:8080`         |
| **Grafana** | `3000`       | Dashboards de métricas/logs/trazas | `http://localhost:3000`         |
| **Jaeger**  | `16686`      | Explorador de trazas               | `http://localhost:16686`        |
| **Loki**    | `3100`       | API de logs (sin UI propia)        | `http://localhost:3100/metrics` |
| **Tempo**   | `3200`       | Backend de trazas                  | `http://localhost:3200/metrics` |
| **Mimir**   | `8082`       | Almacenamiento de métricas         | `http://localhost:8082/metrics` |

> ⚠️ **Nota**: Los puertos locales pueden cambiar si ya están ocupados.
> Ajusta el primer número del comando `port-forward` según necesites.

---

## 🔑 Contraseña de ArgoCD

Para obtener la contraseña inicial del usuario `admin`:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d && echo
```

Luego accede en:
👉 [http://localhost:8080](http://localhost:8080)

---

## 🚀 Escalar el Clúster para Ahorro de Costes

Cuando el clúster **no se usa**, podemos **poner las réplicas a 0** para ahorrar recursos.

### 🔻 Escalar a 0 todos los Deployments

```bash
kubectl scale deploy --all -n monitoring --replicas=0
```

Esto detiene todos los pods, dejando solo los objetos definidos.

### 💾 Guardar el número de réplicas original (antes de escalar a 0)

Guarda las réplicas actuales en un archivo:

```bash
kubectl get deploy -n monitoring \
  -o jsonpath='{range .items[*]}{.metadata.name}{"="}{.spec.replicas}{"\n"}{end}' \
  > replicas.txt
```

El archivo tendrá este formato:

```
jaeger=1
jaeger-operator=1
mimir-distributor=1
mimir-minio=1
...
```

### 🔁 Restaurar las réplicas originales

Cuando quieras volver a levantar los servicios:

```bash
while IFS="=" read -r deploy replicas; do
  kubectl scale deploy $deploy -n monitoring --replicas=$replicas
done < replicas.txt
```

---

## 🧩 Descripción de los Componentes

| Componente       | Rol                                                                         |
| ---------------- | --------------------------------------------------------------------------- |
| **Prometheus**   | Recolección de métricas del clúster y las aplicaciones.                     |
| **Grafana**      | Visualización de métricas, logs y trazas en dashboards.                     |
| **Jaeger**       | Sistema de trazas distribuidas para analizar requests entre microservicios. |
| **Tempo**        | Backend de trazas, almacena y sirve trazas para Jaeger/OTel.                |
| **Mimir**        | Almacenamiento de métricas a largo plazo, escalable y multi-tenant.         |
| **Loki**         | Recolección y consulta de logs centralizados.                               |
| **cert-manager** | Emisión automática de certificados TLS.                                     |

---

## ✅ Cómo Testear el Stack de Observabilidad

1. **Métricas**:

   * Abre Grafana → [http://localhost:3000](http://localhost:3000)
   * Login por defecto: `admin / admin` (o el que hayas configurado).
   * Importa un dashboard de Prometheus para ver métricas del cluster.

2. **Logs**:

   * Desde Grafana → Data Sources → Loki.
   * Ejecuta consultas tipo:

     ```
     {app="jaeger"}
     ```

3. **Trazas**:

   * Abre Jaeger → [http://localhost:16686](http://localhost:16686)
   * Busca trazas por servicio o endpoint.

4. **Mimir**:

   * Comprueba el endpoint:
     [http://localhost:8082/metrics](http://localhost:8082/metrics)

5. **Tempo**:

   * Comprueba que recibe trazas en:
     [http://localhost:3200/metrics](http://localhost:3200/metrics)

---

## 💡 Tips

* Para habilitar rápidamente todos los servicios:

  ```bash
  kubectl scale deploy --all -n monitoring --replicas=1
  ```

  *(o ajusta los valores según `replicas.txt`)*

* ArgoCD permite sincronizar los manifiestos con:

  ```bash
  kubectl get applications -n argocd
  ```

* Antes de hacer cambios, **actualiza este README y `replicas.txt`** para mantener un historial claro.

---

