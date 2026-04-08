"""
TIPO DE DATO ABSTRACTO: PILA (Stack)
=====================================
Una Pila es una estructura de datos LIFO (Last In, First Out):
el último elemento en entrar es el primero en salir.

Operaciones fundamentales:
  - push(elemento) → agrega al tope
  - pop()          → elimina y retorna el tope
  - peek()         → consulta el tope sin eliminarlo
  - is_empty()     → verifica si está vacía
  - size()         → retorna la cantidad de elementos

Casos de uso reales:
  - Historial de deshacer (Ctrl+Z)
  - Navegación hacia atrás en el browser
  - Evaluación de expresiones matemáticas
  - Llamadas a funciones (call stack)
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
# IMPLEMENTACIÓN DE LA PILA
# ─────────────────────────────────────────────
class Pila:
    """Implementación de una Pila usando una lista interna."""

    def __init__(self):
        self._datos = []

    def push(self, elemento):
        """Agrega un elemento al tope de la pila."""
        self._datos.append(elemento)

    def pop(self):
        """Elimina y retorna el elemento del tope. Lanza error si está vacía."""
        if self.is_empty():
            raise IndexError("No se puede hacer pop en una pila vacía.")
        return self._datos.pop()

    def peek(self):
        """Retorna el elemento del tope sin eliminarlo."""
        if self.is_empty():
            raise IndexError("La pila está vacía.")
        return self._datos[-1]

    def is_empty(self):
        """Retorna True si la pila no tiene elementos."""
        return len(self._datos) == 0

    def size(self):
        """Retorna el número de elementos en la pila."""
        return len(self._datos)

    def __repr__(self):
        if self.is_empty():
            return "Pila: [vacía]"
        tope = " ← TOPE"
        elementos = [f"  {e}{tope if i == len(self._datos) - 1 else ''}"
                     for i, e in enumerate(self._datos)]
        return "Pila (tope arriba):\n" + "\n".join(reversed(elementos))


# ─────────────────────────────────────────────
# UTILIDAD: visualizar la pila como tabla
# ─────────────────────────────────────────────
def mostrar_pila(pila: Pila, titulo: str = "Estado de la Pila"):
    tabla = Table(title=titulo, show_header=True, header_style="bold magenta")
    tabla.add_column("Posición", justify="center", style="dim")
    tabla.add_column("Elemento", justify="center", style="cyan bold")
    tabla.add_column("", justify="left")

    datos = list(pila._datos)
    for i in range(len(datos) - 1, -1, -1):
        etiqueta = "[bold green]← TOPE[/bold green]" if i == len(datos) - 1 else ""
        tabla.add_row(str(i), str(datos[i]), etiqueta)

    if pila.is_empty():
        tabla.add_row("-", "[italic dim]vacía[/italic dim]", "")

    console.print(tabla)


# ─────────────────────────────────────────────
# DEMO 1: Operaciones básicas
# ─────────────────────────────────────────────
def demo_operaciones_basicas():
    console.print(Panel("[bold yellow]DEMO 1: Operaciones Básicas[/bold yellow]", expand=False))

    pila = Pila()
    console.print(f"\n[dim]Pila recién creada → vacía: {pila.is_empty()}[/dim]")

    # push
    for valor in [10, 20, 30, 40]:
        pila.push(valor)
        console.print(f"  push([cyan]{valor}[/cyan])  →  tamaño={pila.size()}")

    console.print()
    mostrar_pila(pila)

    # peek
    console.print(f"\n  peek() = [bold green]{pila.peek()}[/bold green]  (no elimina)")

    # pop
    console.print()
    for _ in range(3):
        extraido = pila.pop()
        console.print(f"  pop() = [bold red]{extraido}[/bold red]  →  tamaño={pila.size()}")

    console.print()
    mostrar_pila(pila, "Pila después de 3 pop()")


# ─────────────────────────────────────────────
# DEMO 2: Verificar paréntesis balanceados
# ─────────────────────────────────────────────
def parentesis_balanceados(expresion: str) -> bool:
    """Usa una pila para verificar si los paréntesis están balanceados."""
    pila = Pila()
    pares = {')': '(', ']': '[', '}': '{'}

    for char in expresion:
        if char in '([{':
            pila.push(char)
        elif char in ')]}':
            if pila.is_empty() or pila.pop() != pares[char]:
                return False
    return pila.is_empty()


def demo_parentesis():
    console.print(Panel("[bold yellow]DEMO 2: Paréntesis Balanceados[/bold yellow]", expand=False))
    console.print("[dim]Caso de uso clásico: compiladores usan pilas para validar sintaxis[/dim]\n")

    expresiones = [
        "(a + b) * (c - d)",
        "{[()]}",
        "((()))",
        "(a + b]",
        "(()",
        "{[}]",
    ]

    tabla = Table(show_header=True, header_style="bold blue")
    tabla.add_column("Expresión", style="cyan")
    tabla.add_column("¿Balanceada?", justify="center")

    for expr in expresiones:
        resultado = parentesis_balanceados(expr)
        icono = "[bold green]✓ Sí[/bold green]" if resultado else "[bold red]✗ No[/bold red]"
        tabla.add_row(expr, icono)

    console.print(tabla)


# ─────────────────────────────────────────────
# DEMO 3: Simulación del historial "Deshacer"
# ─────────────────────────────────────────────
def demo_deshacer():
    console.print(Panel("[bold yellow]DEMO 3: Simulación de Deshacer (Ctrl+Z)[/bold yellow]", expand=False))
    console.print("[dim]Los editores de texto guardan acciones en una pila para poder deshacer[/dim]\n")

    historial = Pila()
    documento = []

    def escribir(texto):
        documento.append(texto)
        historial.push(("escribir", texto))
        console.print(f"  [green]Escribir:[/green] '{texto}'  →  doc={documento}")

    def deshacer():
        if historial.is_empty():
            console.print("  [red]Nada que deshacer.[/red]")
            return
        accion, dato = historial.pop()
        if accion == "escribir":
            documento.remove(dato)
            console.print(f"  [yellow]Deshacer:[/yellow] se eliminó '{dato}'  →  doc={documento}")

    escribir("Hola")
    escribir("mundo")
    escribir("!!!")
    console.print()
    deshacer()
    deshacer()
    console.print()
    mostrar_pila(historial, "Historial restante")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    console.print(Panel(
        Text("TIPO DE DATO ABSTRACTO\nPILA (Stack) — LIFO", justify="center", style="bold white"),
        style="bold blue",
        expand=False
    ))
    console.print()

    demo_operaciones_basicas()
    console.print()
    demo_parentesis()
    console.print()
    demo_deshacer()
