# Yuma Pay & Escudo Yuma - Plataforma Financiera Integral

Plataforma financiera digital y sistema antifraude en tiempo real para **Yuma Pay S.A. (SEDPE)**, entidad vigilada por la Superintendencia Financiera de Colombia.

---

## 🏛️ Contexto del Ecosistema
- **Entidad:** Yuma Pay S.A. (Sociedad Especializada en Depósitos y Pagos Electrónicos - SEDPE).
- **Usuarios Activos:** ~4,2 millones de clientes (jóvenes, trabajadores independientes y microcomerciantes).
- **Volumen Transaccional:** ~1,8 millones de operaciones diarias.
- **SLA de Seguridad:** Pre-autorización y evaluación de riesgo en menos de 300 ms (P99 245 ms) con capacidad de 150 tx/seg.

---

## 👥 Arquitectura de Doble Perfil

La plataforma integra de manera nativa dos experiencias a través de un conmutador de perfil en tiempo real:

### 1. 👤 Billetera Digital del Usuario (Clientes)
- **Inicio y Resumen Financiero:** Saludo personalizado, saldo disponible con protección visual (ocultar/mostrar), seguro de depósito Fogafín hasta $50M y control del límite mensual exento de 4x1000 ($9.260.000 COP según Decreto 2642/2022).
- **Transferencias Inmediatas (Transfiya):** Envíos por llave de celular, documento (CC/NIT), correo o cuenta Yuma Pay, con verificación preventiva en segundo plano conectada al motor antifraude.
- **Pagos y Cobros con QR:** Escáner interoperable con cámara simulada y generador de código QR para recibir cobros comerciales.
- **Recargas y Depósitos:** Acreditación instantánea vía PSE (todos los bancos) y convenios de efectivo en corresponsales (Efecty, Baloto, SuperGIROS).
- **Pago de Servicios Públicos y Privados:** Catálogo de convenios (Enel, Acueducto, Vanti, Claro, EPM, Tigo) con pago en 1 clic.
- **Tarjeta Débito Virtual (Mastercard SEDPE):** Tarjeta interactiva con visualización de CVV dinámico temporizado, congelamiento temporal inmediato y límites diarios configurables.
- **Historial Completo & Comprobante Digital:** Trazabilidad de transacciones con modal de comprobante bancario imprimible y descargable.
- **Seguridad de la Cuenta:** Gestión biométrica, notificaciones push, registro de dispositivos habituales y cumplimiento SARLAFT.

### 2. 🛡️ Consola de Analistas y Supervisión (Escudo Yuma)
- **A. Panel General (Overview):** Indicadores de rendimiento clave (KPIs), reducción de falsos positivos al 54.2%, tasa de detección del 86.8%, latencia P99 de 142 ms y ahorro proyectado.
- **B. Simulador de Transacciones (Sandbox):** Inyección de transacciones con 12 variables de contexto/comportamiento, evaluación en las 3 capas, aguja de riesgo, explicación local TreeSHAP y waterfall de latencia.
- **C. Consola de Analistas SOC:** Cola de alertas priorizadas con SLA en cuenta regresiva, línea de tiempo de sospecha, visualizador interactivo SVG de grafo de mulas transaccionales y acciones humanas de resolución (Descartar, Desafiar, Confirmar Fraude, Bloqueo Definitivo).
- **D. Motor Antifraude en 3 Capas:** Reglas Dinámicas Versionadas (Capa 1) + Inferencia XGBoost ML ROC AUC 0.94 (Capa 2) + Grafo de Red O(1) (Capa 3).
- **E. Bucle Cerrado de Retroalimentación:** Aritmética del descarte de reglas ruidosas, calibración continua y MLOps con modelo retador en sombra.
- **F. No Discriminación & Cumplimiento:** Auditoría Fairlearn (paridad demográfica, impacto dispar y odds igualados), exclusión de variables protegidas y adhesión a SARLAFT, Habeas Data, Circular Externa 007 (SFC) y PCI DSS.

---

## 🚀 Puesta en Marcha

### Requisitos
- Node.js (v16+)

### Instalación y Ejecución
```bash
# Iniciar servidor local
node server.js
```

La plataforma estará disponible en:
- **Aplicación Web:** `http://localhost:8080`
- **Especificación OpenAPI REST:** `http://localhost:8080/openapi.yaml`

*Nota: La plataforma también cuenta con un motor cliente embebido de contingencia para operar de forma autónoma en modo estático en cualquier navegador web moderno.*
