from fastapi import FastAPI
from pydantic import BaseModel
from health_check import run_all_checks 

app = FastAPI(title="FinTech Nova - Motor de Riesgo", version="1.0.0")

class SolicitudCredito(BaseModel):
    edad: int
    ingresos: float
    deudas: float

@app.get("/status")
def get_status():
    return {"estado": "Operacional", "servidor": "Nodo-01"}

@app.post("/evaluar-riesgo")
def evaluar_riesgo(solicitud: SolicitudCredito):
    score = solicitud.ingresos - solicitud.deudas
    if solicitud.edad < 18:
        resultado = "Rechazado (Menor de edad)"
    elif score > 1000:
        resultado = "Aprobado"
    else:
        resultado = "En Revision"
    return {"resultado": resultado, "score_simulado": score}

@app.get("/datos-financieros/{id_cliente}")
def obtener_historial(id_cliente: int):
    return {"cliente_id": id_cliente, "historial": "Limpio", "score_interno": 750}

from fastapi import FastAPI, HTTPException
# ... (tu código de API existente) ...
# Agrega esta función:
@app.get('/health')
def health_check_endpoint():
    result = run_all_checks()
    if result['status'] == 'unhealthy':
        raise HTTPException(status_code=503, detail=result)
    return result