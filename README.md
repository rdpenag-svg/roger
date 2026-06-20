
# FinTech Nova — Motor de Riesgo Crediticio

> API de evaluacion de creditos — Roslaysoft Consulting

## Integrantes del Grupo

| Nombre | GitHub User | Rol |

|--------|-------------|-----|

| roger peña | @rdpenag | Coordinador |

## Laboratorio 1 — Estado: COMPLETADO

### URL del Codespace
https://studious-broccoli-jrjqpvvw7w4pfqrpp-8000.app.github.dev

### Endpoints disponibles

| Endpoint | Metodo | Descripcion |

|----------|--------|-------------|

| /status | GET | Health check del sistema |

| /evaluar-riesgo | POST | Motor de scoring crediticio |

| /datos-financieros/{id} | GET | Historial (VULNERABLE - Lab 2) |

### Diagrama Arquitectonico As-Is

![Arquitectura As-Is Lab 1](docs/diagramas/arquitectura_as_is_lab1.png)

## Como ejecutar

```bash

pip install -r requirements.txt

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

```
## Laboratorio 2 — Estado: COMPLETADO

### Objetivo
Demostrar hardening de API mediante cabeceras de seguridad HTTP y prevención de SQL Injection usando consultas parametrizadas.

### URL del Codespace
https://cautious-space-funicular-wvrgqp7w5x6gc945-8000.app.github.dev

### Endpoints disponibles

| Endpoint | Metodo | Descripcion |
|----------|--------|-------------|
| /vulnerable/users/{username} | GET | Endpoint vulnerable a SQLi |
| /secure/users/{username} | GET | Endpoint protegido con prepared statements |

### Hallazgos de Seguridad

**Hallazgo 1 - SQL Injection (A03:2021)**
- Endpoint afectado: `/vulnerable/users/{username}`
- Payload usado: `juan' OR '1'='1`
- Impacto: Expuso todos los usuarios incluyendo admin/superadmin
- Remediacion: Endpoint `/secure/` con consultas parametrizadas neutraliza el ataque

**Hallazgo 2 - Cabeceras de Seguridad HTTP**
- Cabeceras implementadas: X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, Strict-Transport-Security, Content-Security-Policy
- Verificacion: securityheaders.com - Calificacion C (limitacion del proxy de Codespaces)

### Como ejecutar

```bash
cd lab2-hardening-sqli
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```
## Laboratorio 3 — Estado: COMPLETADO

### Objetivo
Implementar automatización de procesos mediante scripting (Bash + Python), observabilidad con health checks y contenerización con Docker para lograr un sistema reproducible y auto-gestionable.

### URL del Codespace
https://roger-8000.preview.app.github.dev

### Componentes del Sistema

| Componente | Tecnología | Descripción |
|------------|------------|-------------|
| Backup Automático | Bash Script | Respaldos programados de la base de datos con retención de 7 días |
| Detector de Ataques | Python + Regex | Análisis de logs para detectar SQL Injection |
| Health Check | Python + FastAPI | Monitoreo de base de datos, disco y backups |
| Contenedor | Docker | Empaquetado de toda la aplicación para despliegue reproducible |

### Endpoints Disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| / | GET | Página principal de la API |
| /status | GET | Estado del sistema |
| /health | GET | Health check completo (BD, disco, backups) |
| /docs | GET | Documentación interactiva de FastAPI |

### Scripts Automatizados

| Script | Lenguaje | Función |
|--------|----------|---------|
| `backup_db.sh` | Bash | Respalda database.db con timestamp y limpia backups viejos (>7 días) |
| `log_analyzer.py` | Python | Analiza server.log y detecta intentos de SQL Injection |
| `resource_monitor.sh` | Bash | Monitorea CPU, RAM y espacio en disco (Ejercicio 1) |

### Tareas Programadas (Cron)

```bash
# Backup automático a las 2:00 AM todos los días
0 2 * * * /workspaces/roger/backup_db.sh >> /tmp/backup.log 2>&1

{
    "estado": "saludable",
    "marca de tiempo": "2026-06-20T00:41:06.140488Z",
    "versión": "1.0.0",
    "comprobaciones": {
        "base de datos": {
            "estado": "ok",
            "mensaje": "BD accesible en 0.1ms"
        },
        "disco": {
            "estado": "ok",
            "mensaje": "Disco saludable: 31.7% usado"
        },
        "copia de seguridad": {
            "estado": "ok",
            "mensaje": "Copia de seguridad reciente: backup_2026-06-20_00-04-20.tar.gz"
        }
    }
}