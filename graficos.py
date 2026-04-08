import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import FancyBboxPatch

# ── Paleta de colores corporativa ────────────────────────
AZUL_OSC  = "#1F4E79"
AZUL_MED  = "#2E75B6"
AZUL_CLAR = "#BDD7EE"
VERDE     = "#375623"
VERDE_MED = "#70AD47"
GRIS      = "#F2F2F2"
BLANCO    = "#FFFFFF"

PALETA_TORTA = ["#1F4E79","#2E75B6","#70AD47","#FFC000","#C55A11","#7030A0","#00B0F0"]

OUTPUT_DIR = "output"


def _setup():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.rcParams.update({
        "font.family":     "DejaVu Sans",
        "axes.spines.top":    False,
        "axes.spines.right":  False,
        "axes.grid":          True,
        "grid.color":         "#E0E0E0",
        "grid.linewidth":     0.6,
        "axes.facecolor":     BLANCO,
        "figure.facecolor":   BLANCO,
    })


def grafico_ingresos_mensuales(resumen_mensual) -> str:
    """Barras de ingresos + línea de ganancia por mes."""
    _setup()
    fig, ax = plt.subplots(figsize=(10, 4.5))

    meses     = resumen_mensual["mes"].tolist()
    ingresos  = resumen_mensual["ingreso"].tolist()
    ganancias = resumen_mensual["ganancia"].tolist()
    x = range(len(meses))

    bars = ax.bar(x, ingresos, color=AZUL_MED, width=0.55, label="Ingreso", zorder=3)
    ax2  = ax.twinx()
    ax2.plot(x, ganancias, color=VERDE_MED, marker="o", linewidth=2,
             markersize=5, label="Ganancia", zorder=4)
    ax2.spines["top"].set_visible(False)
    ax2.tick_params(axis="y", labelcolor=VERDE_MED, labelsize=8)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v/1000:.0f}k"))

    # Etiqueta encima de cada barra
    for bar, val in zip(bars, ingresos):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 200,
                f"${val/1000:.1f}k", ha="center", va="bottom", fontsize=7.5,
                color=AZUL_OSC, fontweight="bold")

    ax.set_xticks(list(x))
    ax.set_xticklabels([m[:3] for m in meses], fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v/1000:.0f}k"))
    ax.tick_params(axis="y", labelsize=8)
    ax.set_ylabel("Ingresos", fontsize=9, color=AZUL_MED)
    ax2.set_ylabel("Ganancia", fontsize=9, color=VERDE_MED)
    ax.set_title("Ingresos y ganancias por mes — 2024", fontsize=12,
                 fontweight="bold", color=AZUL_OSC, pad=12)

    # Leyenda combinada
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2,
              loc="upper left", fontsize=8, framealpha=0.8)

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "grafico_mensual.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def grafico_top5_productos(top5_productos) -> str:
    """Barras horizontales con el top 5 de productos por ingreso."""
    _setup()
    fig, ax = plt.subplots(figsize=(9, 3.8))

    productos = top5_productos["producto"].tolist()
    ingresos  = top5_productos["ingreso"].tolist()

    # Nombres cortos para que entren en el eje
    etiquetas = [p.replace(" 4L", "").replace(" 110mm x 6m", "")
                  .replace(" 650W", "").replace(" grano 120", "") for p in productos]

    colores = [AZUL_OSC if i == 0 else AZUL_MED if i == 1 else AZUL_CLAR
               for i in range(len(productos))]

    bars = ax.barh(etiquetas[::-1], ingresos[::-1], color=colores[::-1],
                   height=0.55, zorder=3)

    # Etiqueta dentro/fuera de cada barra
    for bar, val in zip(bars, ingresos[::-1]):
        ax.text(bar.get_width() + 300, bar.get_y() + bar.get_height() / 2,
                f"${val:,.0f}", va="center", ha="left",
                fontsize=8.5, color=AZUL_OSC, fontweight="bold")

    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v/1000:.0f}k"))
    ax.tick_params(axis="both", labelsize=9)
    ax.set_xlabel("Ingreso anual ($)", fontsize=9)
    ax.set_title("Top 5 productos por ingreso — 2024", fontsize=12,
                 fontweight="bold", color=AZUL_OSC, pad=12)
    ax.set_xlim(0, max(ingresos) * 1.18)

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "grafico_top5.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def grafico_categorias(resumen_categoria) -> str:
    """Torta de participación de ingresos por categoría."""
    _setup()
    fig, ax = plt.subplots(figsize=(7, 5))

    categorias = resumen_categoria["categoria"].tolist()
    valores    = resumen_categoria["ingreso"].tolist()
    total      = sum(valores)

    def autopct(pct):
        return f"{pct:.1f}%" if pct > 5 else ""

    wedges, texts, autotexts = ax.pie(
        valores,
        labels=None,
        autopct=autopct,
        colors=PALETA_TORTA[:len(categorias)],
        startangle=140,
        wedgeprops={"linewidth": 1.2, "edgecolor": BLANCO},
        pctdistance=0.78,
    )
    for t in autotexts:
        t.set_fontsize(8.5)
        t.set_color(BLANCO)
        t.set_fontweight("bold")

    # Leyenda con monto
    leyenda = [f"{c}  (${v:,.0f})" for c, v in zip(categorias, valores)]
    ax.legend(wedges, leyenda, loc="lower center",
              bbox_to_anchor=(0.5, -0.18), ncol=2, fontsize=8.5,
              framealpha=0.8, title="Categoría", title_fontsize=9)

    ax.set_title("Participación de ingresos por categoría", fontsize=12,
                 fontweight="bold", color=AZUL_OSC, pad=14)

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "grafico_categorias.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def generar_todos(metricas: dict) -> dict:
    """Genera los 3 gráficos y devuelve sus rutas."""
    return {
        "mensual":     grafico_ingresos_mensuales(metricas["resumen_mensual"]),
        "top5":        grafico_top5_productos(metricas["top5_productos"]),
        "categorias":  grafico_categorias(metricas["resumen_categoria"]),
    }


if __name__ == "__main__":
    from lector import cargar_datos, calcular_metricas
    df = cargar_datos("ventas_demo.xlsx")
    m  = calcular_metricas(df)
    rutas = generar_todos(m)
    for nombre, ruta in rutas.items():
        print(f"  ✓ {nombre:12} → {ruta}")