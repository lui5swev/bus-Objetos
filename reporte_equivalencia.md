# Reporte de Partición de Equivalencia y Valores Límite

Este reporte detalla las clases de equivalencia (CE) y los análisis de valores límite (AVL) para cada una de las funciones principales de los módulos de la aplicación, satisfaciendo el criterio de evaluación respectivo.

## 1. Módulo: DoublyLinkedList (`src/objects/list.py`)

### Función: `append(value)`
*   **Clases de Equivalencia (CE):**
    *   CE1 (Válida): Cadenas de texto no vacías (ej. "A", "Valor normal").
    *   CE2 (Válida): Cadenas de texto muy largas (simulación de límite MAX).
    *   CE3 (Inválida): Valor nulo (`None`, simulando puntero NULL).
    *   CE4 (Válida): Lista previamente vacía vs Lista con elementos.
*   **Valores Límite (AVL):**
    *   Tamaño de la lista previo a la inserción: 0, 1, MAX.

### Función: `get(position)`
*   **Clases de Equivalencia (CE):**
    *   CE1 (Válida): Índices dentro de los límites $0 \le position < size$.
    *   CE2 (Inválida): Índices negativos $position < 0$.
    *   CE3 (Inválida): Índices superiores o iguales al tamaño $position \ge size$.
*   **Valores Límite (AVL):**
    *   `-1` (Justo fuera del límite inferior).
    *   `0` (Límite inferior válido).
    *   `1` (Valor intermedio típico).
    *   `size - 1` (Límite superior válido).
    *   `size` (Justo fuera del límite superior).

### Función: `remove(position)`
*   **Clases de Equivalencia (CE):**
    *   CE1 (Válida): Remover elemento al inicio (índice 0).
    *   CE2 (Válida): Remover elemento al final (índice size-1).
    *   CE3 (Válida): Remover elemento intermedio.
    *   CE4 (Inválida): Índices fuera de rango ($position < 0$ o $position \ge size$).
*   **Valores Límite (AVL):**
    *   `-1`, `0`, `size/2` (intermedio), `size - 1`, `size`.

### Función: `contains(value)`
*   **Clases de Equivalencia (CE):**
    *   CE1 (Válida): Valor existente en la lista.
    *   CE2 (Válida): Valor no existente en la lista.
    *   CE3 (Inválida): Valor `None` (debe retornar `False`).
*   **Valores Límite (AVL):**
    *   Valor al inicio de la lista (match rápido).
    *   Valor al final de la lista (match tardío).
    *   Valor ausente.

### Función: `get_size()`
*   **Clases de Equivalencia (CE):**
    *   CE1: Lista vacía.
    *   CE2: Lista con 1 elemento.
    *   CE3: Lista con múltiples elementos.

---

## 2. Módulo: DynamicStack (`src/objects/stack.py`)

### Función: `push(value)`
*   **Clases de Equivalencia (CE):**
    *   CE1 (Válida): Valores de texto válidos.
    *   CE2 (Inválida): Valor nulo (`None`).
*   **Valores Límite (AVL):**
    *   Pila con tamaño 0 (Push inicial).
    *   Pila con 1 elemento.
    *   Pila grande (MAX elementos).

### Función: `pop()`
*   **Clases de Equivalencia (CE):**
    *   CE1 (Válida): Pila con elementos (se remueve exitosamente).
    *   CE2 (Inválida): Pila vacía (debe retornar error `EMPTY_STRUCTURE`).
*   **Valores Límite (AVL):**
    *   Tamaño pila: 0, 1, MAX.

### Función: `peek()`
*   **Clases de Equivalencia (CE):**
    *   CE1 (Válida): Pila con elementos (se obtiene tope).
    *   CE2 (Inválida): Pila vacía (retorna `EMPTY_STRUCTURE`).

### Función: `is_empty()`
*   **Clases de Equivalencia (CE):**
    *   CE1: Pila con 0 elementos (retorna `True`).
    *   CE2: Pila con >= 1 elementos (retorna `False`).

---

## 3. Módulo: Serializer (`src/protocol/serializer.py`)

### Función: `deserialize(message)`
*   **Clases de Equivalencia (CE):**
    *   CE1 (Válida): Formato exacto `Objeto|Operación|Id|Datos\n`.
    *   CE2 (Inválida): Mensaje sin terminador de salto de línea (`\n`).
    *   CE3 (Inválida): Faltan campos (ej. `Objeto|Operación|Id\n`).
    *   CE4 (Inválida): Campos requeridos vacíos (ej. `|||Data\n`).
    *   CE5 (Inválida): Parámetro nulo (`None`).
*   **Valores Límite (AVL):**
    *   Cadena vacía `""`.
    *   Mensaje mínimo viable `A|B|C|\n` (Datos vacíos).
    *   Mensaje muy largo (MAX buffer ideal).

### Función: `serialize(response_dict)`
*   **Clases de Equivalencia (CE):**
    *   CE1 (Válida): Diccionario con todas las llaves (`object`, `operation`, `id`, `data`).
    *   CE2 (Inválida/Frontera): Diccionario con llaves faltantes (debe manejar vacíos elegantemente).
    *   CE3 (Inválida): Diccionario `None`.
