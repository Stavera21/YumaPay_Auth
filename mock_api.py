"""
Escudo Yuma - Mock API Client & Sandbox Simulator
Compatible con el sandbox del caso (04_Sandbox_API / mock_api.py).
Permite enviar transacciones de prueba sintéticas y evaluar la respuesta del motor.
"""

import json
import urllib.request
import urllib.error
import time

SANDBOX_URL = "http://localhost:8080/api/v1/score"

ESCENARIOS_DE_PRUEBA = [
    {
        "nombre": "1. Toma de Cuenta (Phishing)",
        "payload": {
            "transaccion_id": "TX-ATO-001",
            "cuenta_origen": "CTA-88310",
            "cuenta_destino": "CTA-99231",
            "monto": 950000,
            "tipo_operacion": "TRANSFERENCIA_INMEDIATA",
            "canal": "APP_MOVIL",
            "dispositivo_nuevo": True,
            "cambio_clave_24h": True,
            "cambio_sim_48h": False,
            "time_to_cash_minutos": 3.2,
            "monto_p95_90d": 150000,
            "saldo_actual": 980000,
            "es_madrugada": False
        },
        "esperado": "RETENER"
    },
    {
        "nombre": "2. SIM Swapping Agresivo",
        "payload": {
            "transaccion_id": "TX-SIM-002",
            "cuenta_origen": "CTA-44120",
            "cuenta_destino": "CTA-77812",
            "monto": 1450000,
            "tipo_operacion": "TRANSFERENCIA_INMEDIATA",
            "canal": "APP_MOVIL",
            "dispositivo_nuevo": True,
            "cambio_clave_24h": False,
            "cambio_sim_48h": True,
            "time_to_cash_minutos": 6.8,
            "monto_p95_90d": 200000,
            "saldo_actual": 1500000,
            "es_madrugada": True
        },
        "esperado": "RETENER"
    },
    {
        "nombre": "3. Red de Cuenta Mula (Fan-In Alto)",
        "payload": {
            "transaccion_id": "TX-MULE-003",
            "cuenta_origen": "CTA-12005",
            "cuenta_destino": "CTA-MULA-007",  # Cuenta mula confirmada
            "monto": 780000,
            "tipo_operacion": "TRANSFERENCIA_INMEDIATA",
            "canal": "APP_MOVIL",
            "dispositivo_nuevo": False,
            "cambio_clave_24h": False,
            "cambio_sim_48h": False,
            "time_to_cash_minutos": 45.0,
            "monto_p95_90d": 500000,
            "saldo_actual": 850000,
            "es_madrugada": False
        },
        "esperado": "RETENER / RECHAZAR"
    },
    {
        "nombre": "4. Ingeniería Social (Cliente persuadido, sin cambio de aparato)",
        "payload": {
            "transaccion_id": "TX-SOCENG-004",
            "cuenta_origen": "CTA-55910",
            "cuenta_destino": "CTA-98102",
            "monto": 1800000,
            "tipo_operacion": "TRANSFERENCIA_INMEDIATA",
            "canal": "APP_MOVIL",
            "dispositivo_nuevo": False,
            "cambio_clave_24h": False,
            "cambio_sim_48h": False,
            "time_to_cash_minutos": 22.0,
            "monto_p95_90d": 120000, # Gran desvío de patrón
            "saldo_actual": 1820000, # Vaciado de saldo
            "es_madrugada": False
        },
        "esperado": "RETENER (para confirmación fuera de banda)"
    },
    {
        "nombre": "5. Transacción Habitual Legítima",
        "payload": {
            "transaccion_id": "TX-LEGIT-005",
            "cuenta_origen": "CTA-33100",
            "cuenta_destino": "CTA-44200",
            "monto": 45000,
            "tipo_operacion": "TRANSFERENCIA_INMEDIATA",
            "canal": "APP_MOVIL",
            "dispositivo_nuevo": False,
            "cambio_clave_24h": False,
            "cambio_sim_48h": False,
            "time_to_cash_minutos": 120.0,
            "monto_p95_90d": 95000,
            "saldo_actual": 650000,
            "es_madrugada": False
        },
        "esperado": "APROBAR"
    }
]

def evaluar_transaccion(payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        SANDBOX_URL,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            t_ms = (time.time() - t0) * 1000
            res_json = json.loads(resp.read().decode("utf-8"))
            return res_json, t_ms
    except urllib.error.URLError as e:
        return {"error": str(e)}, 0

if __name__ == "__main__":
    print("=== Sandbox Escudo Yuma - Ejecución de Casos de Prueba ===")
    for c in ESCENARIOS_DE_PRUEBA:
        print(f"\nProbando escenario: {c['nombre']}")
        res, t_elapsed = evaluar_transaccion(c["payload"])
        if "error" in res:
            print(f"❌ Error al conectar al servicio: {res['error']}")
        else:
            print(f"  Resultado: {res.get('decision')} | Score: {res.get('score_riesgo')}/1000 | Tramo: {res.get('tramo_riesgo')}")
            print(f"  Latencia reportada: {res.get('presupuesto_latencia_ms', {}).get('latencia_total_ms')} ms (HTTP RTT: {t_elapsed:.1f} ms)")
            print(f"  Códigos de razón: {[r['codigo'] for r in res.get('explicacion', {}).get('codigos_razon', [])]}")
            print(f"  Cumple SLA < 300ms: {res.get('presupuesto_latencia_ms', {}).get('cumple_sla_300ms')}")
