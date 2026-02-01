# TEST CONTRACT — Reconcile Rendition

Este documento define el contrato de pruebas para el feature
**Reconcile Rendition (Cuadrar Rendición)**, derivado exclusivamente
de la `SPEC_RECONCILE_RENDITION.md`.

---

## 1. Unidad bajo prueba

La implementación debe exponer una única función pura:

```python
def reconcile_rendition(
    system_amounts: dict,
    declared_amounts: dict
) -> dict:
    ...
```

---

## 2. Input contract

### 2.1 system_amounts (por rendir)

```python
{
  "cash": float,
  "debit_card": float,
  "credit_card": float
}
```

Representa los montos registrados por el sistema.

---

### 2.2 declared_amounts (rendido)

```python
{
  "cash": float,
  "debit_card": float,
  "credit_card": float
}
```

Representa los montos ingresados manualmente por el cajero.

---

## 3. Output contract

```python
{
  "status": str,              # BALANCED | UNBALANCED
  "differences": {
    "cash": float,
    "debit_card": float,
    "credit_card": float
  }
}
```

---

## 4. Semántica de diferencias

Para cada medio de pago:

```
difference = declared_amount - system_amount
```

- `0` → sin diferencia  
- `> 0` → sobrante  
- `< 0` → faltante  

---

## 5. Status global

- `BALANCED` → todas las diferencias son exactamente `0`
- `UNBALANCED` → existe al menos una diferencia distinta de `0`

No existe tolerancia.

---

## 6. Casos de prueba obligatorios

### 6.1 Rendición completamente cuadrada

```python
system = {"cash": 100, "debit_card": 200, "credit_card": 300}
declared = {"cash": 100, "debit_card": 200, "credit_card": 300}
```

Resultado esperado:
- status = `BALANCED`
- todas las diferencias = `0`

---

### 6.2 Sobrante en efectivo

```python
system = {"cash": 100, "debit_card": 200, "credit_card": 300}
declared = {"cash": 120, "debit_card": 200, "credit_card": 300}
```

Resultado esperado:
- status = `UNBALANCED`
- cash = `+20`

---

### 6.3 Faltante en tarjeta débito

```python
system = {"cash": 100, "debit_card": 200, "credit_card": 300}
declared = {"cash": 100, "debit_card": 180, "credit_card": 300}
```

Resultado esperado:
- debit_card = `-20`

---

### 6.4 Diferencias en múltiples medios

```python
system = {"cash": 100, "debit_card": 200, "credit_card": 300}
declared = {"cash": 90, "debit_card": 220, "credit_card": 300}
```

Resultado esperado:
- cash = `-10`
- debit_card = `+20`
- credit_card = `0`

---

### 6.5 Todas las diferencias negativas

```python
system = {"cash": 100, "debit_card": 200, "credit_card": 300}
declared = {"cash": 80, "debit_card": 150, "credit_card": 250}
```

Resultado esperado:
- status = `UNBALANCED`
- todas las diferencias < `0`

---

## 7. Reglas explícitas

La implementación **NO debe**:

- Persistir datos
- Corregir montos
- Generar asientos contables
- Notificar
- Modificar los inputs
- Depender de estado previo

---

## 8. Casos fuera de alcance (NO TESTEAR)

- Otros medios de pago
- Validaciones de tipo o rango
- Persistencia
- Integraciones externas
- Side effects

---

## 9. Naturaleza del contrato

Este documento es un **contrato estricto**.
Si todos los tests derivados de este contrato pasan,
la implementación se considera correcta.
