# Tipos de Datos Abstractos (TDA)

Scripts educativos para demostrar los Tipos de Datos Abstractos más importantes en Python. Cada archivo es independiente y puede ejecutarse por separado.

## ¿Qué es un Tipo de Dato Abstracto?

Un **Tipo de Dato Abstracto (TDA)** define una estructura de datos por su **comportamiento** (operaciones que soporta), no por su implementación interna. Esto permite cambiar la implementación sin afectar el código que la usa.

## Scripts incluidos

### `pilas.py` — Pila (Stack)

Estructura **LIFO** (Last In, First Out): el último en entrar es el primero en salir.

| Operación | Descripción | Complejidad |
|-----------|-------------|-------------|
| `push(e)` | Agrega al tope | O(1) |
| `pop()` | Elimina y retorna el tope | O(1) |
| `peek()` | Consulta el tope sin eliminar | O(1) |
| `is_empty()` | Verifica si está vacía | O(1) |
| `size()` | Cantidad de elementos | O(1) |

**Demos incluidas:**
- Operaciones básicas con tabla visual
- Verificador de paréntesis balanceados (como lo hacen los compiladores)
- Simulación del historial Deshacer (Ctrl+Z)

---

### `colas.py` — Cola (Queue)

Estructura **FIFO** (First In, First Out): el primero en entrar es el primero en salir.

| Operación | Descripción | Complejidad |
|-----------|-------------|-------------|
| `enqueue(e)` | Agrega al final | O(1) |
| `dequeue()` | Elimina y retorna el frente | O(1) |
| `front()` | Consulta el frente sin eliminar | O(1) |
| `is_empty()` | Verifica si está vacía | O(1) |
| `size()` | Cantidad de elementos | O(1) |

**Demos incluidas:**
- Operaciones básicas con tabla visual
- Sistema de tickets de atención al cliente
- Cola de prioridad: sala de urgencias médicas

---

### `diccionarios.py` — Diccionario (Hash Map)

Estructura de pares **clave → valor** con acceso en tiempo constante promedio, implementada como tabla hash con encadenamiento para resolver colisiones.

| Operación | Descripción | Complejidad |
|-----------|-------------|-------------|
| `put(k, v)` | Inserta o actualiza | O(1) prom. |
| `get(k)` | Retorna el valor de la clave | O(1) prom. |
| `delete(k)` | Elimina la entrada | O(1) prom. |
| `contains(k)` | Verifica si la clave existe | O(1) prom. |
| `keys()` / `values()` | Retorna claves o valores | O(n) |

**Demos incluidas:**
- Operaciones básicas con visualización de índices hash
- Estructura interna de buckets y colisiones
- Conteo de frecuencias de palabras
- Memoización de Fibonacci con caché

---

## Requisitos y ejecución

Este proyecto usa [uv](https://docs.astral.sh/uv/) para gestión de dependencias.

```bash
# Instalar dependencias
uv sync

# Ejecutar cada script
uv run python pilas.py
uv run python colas.py
uv run python diccionarios.py
```

**Dependencias:** `rich` (visualización en terminal con tablas y colores)

## Estructura del proyecto

```
Tipos-de-Datos/
├── pilas.py          # TDA Pila (Stack — LIFO)
├── colas.py          # TDA Cola (Queue — FIFO)
├── diccionarios.py   # TDA Diccionario (Hash Map)
├── pyproject.toml    # Configuración del proyecto (uv)
└── README.md
```
