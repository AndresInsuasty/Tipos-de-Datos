"""
TIPO DE DATO ABSTRACTO: COLA (Queue)
======================================
Una Cola es una estructura de datos FIFO (First In, First Out):
el primer elemento en entrar es el primero en salir.

Operaciones fundamentales:
  - enqueue(elemento) → agrega al final
  - dequeue()         → elimina y retorna el frente
  - front()           → consulta el frente sin eliminarlo
  - is_empty()        → verifica si está vacía
  - size()            → retorna la cantidad de elementos

Casos de uso reales:
  - Cola de impresión de documentos
  - Manejo de solicitudes en un servidor web
  - BFS (búsqueda en anchura) en grafos
  - Sistemas de tickets / atención al cliente
"""

import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from collections import deque
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console(force_terminal=True, highlight=False)


# ─────────────────────────────────────────────
# IMPLEMENTACIÓN DE LA COLA
# ─────────────────────────────────────────────
class Cola:
    """
    Implementación de una Cola usando collections.deque internamente.
    deque permite O(1) en ambos extremos, a diferencia de una lista común.
    """

    def __init__(self):
        self._datos = deque()

    def enqueue(self, elemento):
        """Agrega un elemento al final de la cola."""
        self._datos.append(elemento)

    def dequeue(self):
        """Elimina y retorna el elemento del frente. Lanza error si está vacía."""
        if self.is_empty():
            raise IndexError("No se puede hacer dequeue en una cola vacía.")
        return self._datos.popleft()

    def front(self):
        """Retorna el elemento del frente sin eliminarlo."""
        if self.is_empty():
            raise IndexError("La cola está vacía.")
        return self._datos[0]

    def is_empty(self):
        """Retorna True si la cola no tiene elementos."""
        return len(self._datos) == 0

    def size(self):
        """Retorna el número de elementos en la cola."""
        return len(self._datos)

    def __repr__(self):
        if self.is_empty():
            return "Cola: [vacía]"
        elementos = list(self._datos)
        return "Cola: FRENTE → " + " → ".join(str(e) for e in elementos) + " ← FINAL"


# ─────────────────────────────────────────────
# IMPLEMENTACIÓN DE COLA DE PRIORIDAD
# ─────────────────────────────────────────────
class ColaDePrioridad:
    """
    Cola donde cada elemento tiene una prioridad.
    El elemento con MAYOR prioridad (número menor) sale primero.
    Implementación simple con lista ordenada (O(n) inserción).
    """

    def __init__(self):
        self._datos = []  # lista de tuplas (prioridad, elemento)

    def enqueue(self, elemento, prioridad: int):
        self._datos.append((prioridad, elemento))
        self._datos.sort(key=lambda x: x[0])  # mantener orden

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Cola de prioridad vacía.")
        prioridad, elemento = self._datos.pop(0)
        return elemento, prioridad

    def front(self):
        if self.is_empty():
            raise IndexError("Cola de prioridad vacía.")
        return self._datos[0]

    def is_empty(self):
        return len(self._datos) == 0

    def size(self):
        return len(self._datos)


# ─────────────────────────────────────────────
# UTILIDAD: visualizar la cola como tabla
# ─────────────────────────────────────────────
def mostrar_cola(cola: Cola, titulo: str = "Estado de la Cola"):
    tabla = Table(title=titulo, show_header=True, header_style="bold magenta")
    tabla.add_column("Posición", justify="center", style="dim")
    tabla.add_column("Elemento", justify="center", style="cyan bold")
    tabla.add_column("", justify="left")

    datos = list(cola._datos)
    for i, elemento in enumerate(datos):
        if i == 0:
            etiqueta = "[bold green]← FRENTE (sale primero)[/bold green]"
        elif i == len(datos) - 1:
            etiqueta = "[bold blue]← FINAL (entra aquí)[/bold blue]"
        else:
            etiqueta = ""
        tabla.add_row(str(i), str(elemento), etiqueta)

    if cola.is_empty():
        tabla.add_row("-", "[italic dim]vacía[/italic dim]", "")

    console.print(tabla)


# ─────────────────────────────────────────────
# DEMO 1: Operaciones básicas
# ─────────────────────────────────────────────
def demo_operaciones_basicas():
    console.print(Panel("[bold yellow]DEMO 1: Operaciones Básicas[/bold yellow]", expand=False))

    cola = Cola()
    console.print(f"\n[dim]Cola recién creada → vacía: {cola.is_empty()}[/dim]")

    # enqueue
    for valor in ["A", "B", "C", "D"]:
        cola.enqueue(valor)
        console.print(f"  enqueue([cyan]'{valor}'[/cyan])  →  tamaño={cola.size()}")

    console.print()
    mostrar_cola(cola)

    # front
    console.print(f"\n  front() = [bold green]'{cola.front()}'[/bold green]  (no elimina)")

    # dequeue
    console.print()
    for _ in range(3):
        extraido = cola.dequeue()
        console.print(f"  dequeue() = [bold red]'{extraido}'[/bold red]  →  tamaño={cola.size()}")

    console.print()
    mostrar_cola(cola, "Cola después de 3 dequeue()")


# ─────────────────────────────────────────────
# DEMO 2: Simulación cola de atención al cliente
# ─────────────────────────────────────────────
def demo_atencion_cliente():
    console.print(Panel("[bold yellow]DEMO 2: Sistema de Tickets — Atención al Cliente[/bold yellow]", expand=False))
    console.print("[dim]Cada cliente toma un número y espera ser llamado en orden[/dim]\n")

    cola = Cola()
    clientes = ["María", "Juan", "Pedro", "Lucía", "Carlos"]

    # Llegan los clientes
    console.print("[bold]Clientes llegando al banco:[/bold]")
    for i, nombre in enumerate(clientes, start=1):
        cola.enqueue(f"Ticket #{i} — {nombre}")
        console.print(f"  [green]+[/green] {nombre} tomó el Ticket #{i}  (en espera: {cola.size()})")

    console.print()
    mostrar_cola(cola, "Cola de espera")

    # Se atienden los clientes
    console.print("\n[bold]Llamando clientes en orden:[/bold]")
    turno = 1
    while not cola.is_empty():
        cliente = cola.dequeue()
        console.print(f"  [bold cyan]Ventanilla {turno}:[/bold cyan] Atendiendo a {cliente}  (quedan: {cola.size()})")
        turno += 1


# ─────────────────────────────────────────────
# DEMO 3: Cola de prioridad — urgencias médicas
# ─────────────────────────────────────────────
def demo_cola_prioridad():
    console.print(Panel("[bold yellow]DEMO 3: Cola de Prioridad — Urgencias[/bold yellow]", expand=False))
    console.print("[dim]Prioridad 1 = crítico, 2 = urgente, 3 = moderado, 4 = leve[/dim]\n")

    sala = ColaDePrioridad()
    pacientes = [
        ("Roberto — fractura de brazo", 3),
        ("Elena — infarto",             1),
        ("Luis — dolor de cabeza",      4),
        ("Ana — apendicitis",           2),
        ("Sofía — fiebre alta",         3),
    ]

    console.print("[bold]Llegada de pacientes:[/bold]")
    for paciente, prioridad in pacientes:
        sala.enqueue(paciente, prioridad)
        etiqueta = {1: "🔴 CRÍTICO", 2: "🟠 URGENTE", 3: "🟡 MODERADO", 4: "🟢 LEVE"}[prioridad]
        console.print(f"  [dim]+[/dim] {paciente}  [{etiqueta}]")

    console.print("\n[bold]Orden de atención por prioridad:[/bold]")
    tabla = Table(show_header=True, header_style="bold red")
    tabla.add_column("#", justify="center", style="dim")
    tabla.add_column("Paciente", style="cyan")
    tabla.add_column("Prioridad", justify="center")

    orden = 1
    while not sala.is_empty():
        paciente, prioridad = sala.dequeue()
        etiqueta = {1: "[red]1 — CRÍTICO[/red]", 2: "[orange3]2 — URGENTE[/orange3]",
                    3: "[yellow]3 — MODERADO[/yellow]", 4: "[green]4 — LEVE[/green]"}[prioridad]
        tabla.add_row(str(orden), paciente, etiqueta)
        orden += 1

    console.print(tabla)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    console.print(Panel(
        Text("TIPO DE DATO ABSTRACTO\nCOLA (Queue) — FIFO", justify="center", style="bold white"),
        style="bold green",
        expand=False
    ))
    console.print()

    demo_operaciones_basicas()
    console.print()
    demo_atencion_cliente()
    console.print()
    demo_cola_prioridad()
