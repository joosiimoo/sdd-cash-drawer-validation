# SPEC — Reconcile Rendition (Cuadrar Rendición)

## 1. Objetivo

Validar la rendición de una caja (POS) para un día específico, comparando los montos
registrados por el sistema versus los montos rendidos por el cajero, y entregar un
estado global indicando si existen diferencias.

Este feature no corrige, no persiste, no notifica y no genera efectos contables.

---

## 2. Actor

Cajero

El cajero ingresa los montos rendidos por medio de pago y ejecuta la validación.

---

## 3. Alcance temporal

La validación aplica siempre a una única combinación de:

- Caja (POS)
- Fecha (día calendario)

No considera turnos, ni múltiples días, ni agregaciones entre cajas.

---

## 4. Flujo temporal

- El cajero puede ejecutar la validación múltiples veces.
- Cada ejecución es independiente.
- El resultado no implica cierre de caja ni bloqueo de nuevas ejecuciones.

---

## 5. Definiciones clave

### 5.1 Por rendir (system amounts)

Corresponde a los montos de ventas registrados por el sistema,
por medio de pago, para la caja y fecha.

Es el source of truth del sistema.

Incluye:
- Ventas efectivas registradas

Excluye:
- Ajustes manuales
- Correcciones
- Procesos contables

---

### 5.2 Rendido (declared amounts)

Corresponde a los montos ingresados manualmente por el cajero,
desglosados por medio de pago.

El sistema no valida el origen de estos montos.

---

## 6. Medios de pago soportados

Este feature solo considera los siguientes medios:

- cash
- debit_card
- credit_card

Cualquier otro medio de pago no existe para esta validación.

---

## 7. Diferencias

### 7.1 Definición

Para cada medio de pago:

difference = declared_amount - system_amount

---

### 7.2 Clasificación

- difference = 0 → sin diferencia
- difference > 0 → sobrante
- difference < 0 → faltante

No existe tolerancia.
Cualquier diferencia distinta de 0 es considerada error.

---

## 8. Resultado

El feature entrega un único estado global:

- BALANCED → no existen diferencias en ningún medio de pago
- UNBALANCED → existe al menos una diferencia

No se entregan estados parciales por medio de pago como resultado principal.

---

## 9. Finalización del proceso

El proceso se considera finalizado cuando el sistema ejecuta la validación
y devuelve el resultado.

No requiere confirmación adicional del usuario.

---

## 10. Exclusiones explícitas (NO hace)

Este feature NO:

- Corrige la rendición
- Genera asientos contables
- Persiste histórico
- Notifica a otros sistemas o usuarios

---

## 11. Notas de diseño

- El feature debe ser determinístico
- No depende de estado previo
- No modifica datos
- Puede ejecutarse repetidamente sin efectos colaterales

---

## 12. Estado de la spec

- Ambigüedades cerradas
- Dependencias implícitas eliminadas
- Lista para generación de test contract e implementación
