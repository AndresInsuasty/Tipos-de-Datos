"""
TIPO DE DATO ABSTRACTO: DICCIONARIO (Map / Hash Map)
======================================================
Un Diccionario (también llamado Mapa o Tabla Hash) almacena pares
clave → valor. Permite acceso, inserción y eliminación en O(1) promedio.

Operaciones fundamentales:
  - put(clave, valor)  → inserta o actualiza
  - get(clave)         → retorna el valor asociado
  - delete(clave)      → elimina la entrada
  - contains(clave)    → verifica si la clave existe
  - keys()             → retorna todas las claves
  - values()           → retorna todos los valores
  - size()             → retorna la cantidad de entradas

Concepto clave — función de hash:
  La clave se pasa por una función hash que devuelve un índice
  dentro de un arreglo interno. Esto hace que el acceso sea O(1).

Casos de uso reales:
  - Caché / memoización
  - Conteo de frecuencias
  - Índices de bases de datos
  - Traducción de símbolos (compiladores)
"""

import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console(force_terminal=True, highlight=False)


# ─────────────────────────────────────────────
# IMPLEMENTACIÓN: Tabla Hash con encadenamiento
# ─────────────────────────────────────────────
class DiccionarioHash:
    """
    Implementación de un Diccionario usando una Tabla Hash.
    Colisiones se resuelven por encadenamiento (chaining):
    cada slot del arreglo contiene una lista de pares (clave, valor).
    """

    def __init__(self, capacidad: int = 8):
        self._capacidad = capacidad
        self._buckets: list[list] = [[] for _ in range(capacidad)]
        self._tamanio = 0

    # ── función de hash ──────────────────────
    def _hash(self, clave) -> int:
        """Convierte una clave en un índice del arreglo interno."""
        return hash(clave) % self._capacidad

    # ── put ──────────────────────────────────
    def put(self, clave, valor):
        """Inserta o actualiza la clave con el valor dado."""
        indice = self._hash(clave)
        bucket = self._buckets[indice]

        for i, (k, v) in enumerate(bucket):
            if k == clave:
                bucket[i] = (clave, valor)  # actualizar
                return

        bucket.append((clave, valor))        # insertar nuevo
        self._tamanio += 1

    # ── get ──────────────────────────────────
    def get(self, clave, default=None):
        """Retorna el valor asociado a la clave, o default si no existe."""
        indice = self._hash(clave)
        for k, v in self._buckets[indice]:
            if k == clave:
                return v
        return default

    # ── delete ───────────────────────────────
    def delete(self, clave):
        """Elimina la entrada con esa clave. Lanza error si no existe."""
        indice = self._hash(clave)
        bucket = self._buckets[indice]
        for i, (k, v) in enumerate(bucket):
            if k == clave:
                del bucket[i]
                self._tamanio -= 1
                return
        raise KeyError(f"La clave '{clave}' no existe.")

    # ── contains ─────────────────────────────
    def contains(self, clave) -> bool:
        return self.get(clave, _SENTINEL) is not _SENTINEL

    # ── keys / values / items ─────────────────
    def keys(self):
        return [k for bucket in self._buckets for k, v in bucket]

    def values(self):
        return [v for bucket in self._buckets for k, v in bucket]

    def items(self):
        return [(k, v) for bucket in self._buckets for k, v in bucket]

    def size(self):
        return self._tamanio

    def is_empty(self):
        return self._tamanio == 0

    # ── soporte para [] ──────────────────────
    def __setitem__(self, clave, valor):
        self.put(clave, valor)

    def __getitem__(self, clave):
        resultado = self.get(clave, _SENTINEL)
        if resultado is _SENTINEL:
            raise KeyError(f"La clave '{clave}' no existe.")
        return resultado

    def __contains__(self, clave):
        return self.contains(clave)

    def __repr__(self):
        pares = ", ".join(f"{k!r}: {v!r}" for k, v in self.items())
        return "{" + pares + "}"


_SENTINEL = object()  # objeto único para detectar ausencia de clave


# ─────────────────────────────────────────────
# UTILIDADES VISUALES
# ─────────────────────────────────────────────
def mostrar_diccionario(d: DiccionarioHash, titulo: str = "Diccionario"):
    tabla = Table(title=titulo, show_header=True, header_style="bold magenta")
    tabla.add_column("Clave", style="cyan bold", justify="center")
    tabla.add_column("Valor", style="white", justify="center")
    tabla.add_column("Índice hash (bucket)", style="dim", justify="center")

    for k, v in sorted(d.items(), key=lambda x: str(x[0])):
        indice = d._hash(k)
        tabla.add_row(str(k), str(v), str(indice))

    if d.is_empty():
        tabla.add_row("[italic dim]vacío[/italic dim]", "", "")

    console.print(tabla)


def mostrar_buckets_internos(d: DiccionarioHash):
    """Muestra la estructura interna del arreglo de buckets."""
    tabla = Table(title="Estructura Interna (buckets)", show_header=True, header_style="bold blue")
    tabla.add_column("Índice", justify="center", style="dim")
    tabla.add_column("Contenido del bucket", style="yellow")

    for i, bucket in enumerate(d._buckets):
        if bucket:
            contenido = "  →  ".join(f"({k!r}: {v!r})" for k, v in bucket)
        else:
            contenido = "[dim]vacío[/dim]"
        tabla.add_row(str(i), contenido)

    console.print(tabla)


# ─────────────────────────────────────────────
# DEMO 1: Operaciones básicas
# ─────────────────────────────────────────────
def demo_operaciones_basicas():
    console.print(Panel("[bold yellow]DEMO 1: Operaciones Básicas[/bold yellow]", expand=False))

    d = DiccionarioHash()

    # put
    datos = [("nombre", "Andrés"), ("edad", 21), ("carrera", "Sistemas"), ("semestre", 4)]
    console.print("\n[bold]Insertando pares clave-valor:[/bold]")
    for clave, valor in datos:
        d.put(clave, valor)
        console.print(f"  put([cyan]'{clave}'[/cyan], [green]{valor!r}[/green])")

    console.print()
    mostrar_diccionario(d, "Diccionario — estudiante")

    # get
    console.print(f"\n  get('nombre')  = [bold green]{d.get('nombre')!r}[/bold green]")
    console.print(f"  get('ciudad')  = [bold red]{d.get('ciudad', 'NO ENCONTRADO')!r}[/bold red]  (clave inexistente)")

    # contains
    console.print(f"\n  'edad' in d    → [bold]{'edad' in d}[/bold]")
    console.print(f"  'altura' in d  → [bold]{'altura' in d}[/bold]")

    # actualizar
    d.put("semestre", 5)
    console.print(f"\n  put('semestre', 5)  →  ahora semestre = [bold cyan]{d['semestre']}[/bold cyan]")

    # delete
    d.delete("carrera")
    console.print(f"  delete('carrera')  →  tamaño={d.size()}")
    console.print()
    mostrar_diccionario(d, "Diccionario después de delete")


# ─────────────────────────────────────────────
# DEMO 2: Colisiones y estructura interna
# ─────────────────────────────────────────────
def demo_colisiones():
    console.print(Panel("[bold yellow]DEMO 2: Colisiones — Estructura Interna de la Tabla Hash[/bold yellow]", expand=False))
    console.print("[dim]Con una capacidad pequeña es fácil ver cómo varias claves\ncaen en el mismo bucket y se encadenan.[/dim]\n")

    # Capacidad 4 → más colisiones visibles
    d = DiccionarioHash(capacidad=4)
    paises = {"CO": "Colombia", "MX": "México", "AR": "Argentina",
              "BR": "Brasil", "PE": "Perú", "CL": "Chile"}

    for codigo, pais in paises.items():
        d.put(codigo, pais)

    mostrar_buckets_internos(d)
    console.print(f"\n[dim]Total entradas: {d.size()}  |  Capacidad: {d._capacidad} buckets[/dim]")


# ─────────────────────────────────────────────
# DEMO 3: Conteo de frecuencias de palabras
# ─────────────────────────────────────────────
def demo_frecuencias():
    console.print(Panel("[bold yellow]DEMO 3: Conteo de Frecuencias de Palabras[/bold yellow]", expand=False))
    console.print("[dim]Caso de uso clásico: contar cuántas veces aparece cada palabra[/dim]\n")

    texto = (
        "el algoritmo usa una tabla hash y la tabla hash "
        "guarda cada clave con su valor el valor puede ser "
        "cualquier tipo de dato y la clave debe ser única"
    )

    console.print(f"[italic]Texto:[/italic] \"{texto}\"\n")

    frecuencias = DiccionarioHash()
    for palabra in texto.split():
        conteo_actual = frecuencias.get(palabra, 0)
        frecuencias.put(palabra, conteo_actual + 1)

    # Ordenar por frecuencia descendente
    tabla = Table(title="Frecuencia de palabras", show_header=True, header_style="bold cyan")
    tabla.add_column("Palabra", style="cyan")
    tabla.add_column("Frecuencia", justify="center")
    tabla.add_column("Barra", style="green")

    items_ordenados = sorted(frecuencias.items(), key=lambda x: -x[1])
    for palabra, conteo in items_ordenados:
        barra = "█" * conteo
        tabla.add_row(palabra, str(conteo), barra)

    console.print(tabla)


# ─────────────────────────────────────────────
# DEMO 4: Caché / Memoización con diccionario
# ─────────────────────────────────────────────
def demo_cache():
    console.print(Panel("[bold yellow]DEMO 4: Caché con Memoización — Fibonacci[/bold yellow]", expand=False))
    console.print("[dim]Un diccionario guarda resultados ya calculados para no repetir trabajo[/dim]\n")

    cache = DiccionarioHash()
    llamadas_totales = [0]

    def fib(n: int) -> int:
        llamadas_totales[0] += 1
        if n in cache:
            console.print(f"  [dim]fib({n}) → HIT caché[/dim]")
            return cache[n]
        if n <= 1:
            resultado = n
        else:
            resultado = fib(n - 1) + fib(n - 2)
        cache[n] = resultado
        return resultado

    console.print("[bold]Calculando fib(0) a fib(10):[/bold]")
    resultados = [(i, fib(i)) for i in range(11)]

    tabla = Table(show_header=True, header_style="bold magenta")
    tabla.add_column("n", justify="center", style="cyan")
    tabla.add_column("fib(n)", justify="center", style="bold white")

    for n, val in resultados:
        tabla.add_row(str(n), str(val))

    console.print(tabla)
    console.print(f"\n[dim]Llamadas a fib() en total: {llamadas_totales[0]}[/dim]")
    console.print(f"[dim]Sin caché serían ~{2**10} llamadas para fib(10)[/dim]")
    console.print(f"\n[dim]Estado final del caché:[/dim]")
    mostrar_diccionario(cache, "Caché de Fibonacci")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    console.print(Panel(
        Text("TIPO DE DATO ABSTRACTO\nDICCIONARIO (Hash Map)", justify="center", style="bold white"),
        style="bold magenta",
        expand=False
    ))
    console.print()

    demo_operaciones_basicas()
    console.print()
    demo_colisiones()
    console.print()
    demo_frecuencias()
    console.print()
    demo_cache()
