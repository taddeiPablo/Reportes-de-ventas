import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# ── Colores ──────────────────────────────────────────────
AZUL_OSC   = colors.HexColor("#1F4E79")
AZUL_MED   = colors.HexColor("#2E75B6")
AZUL_CLAR  = colors.HexColor("#BDD7EE")
VERDE_MED  = colors.HexColor("#70AD47")
AMARILLO   = colors.HexColor("#FFC000")
GRIS_CLAR  = colors.HexColor("#F2F2F2")
GRIS_MED   = colors.HexColor("#D9D9D9")
BLANCO     = colors.white
NEGRO      = colors.HexColor("#1A1A1A")

OUTPUT_DIR = "output"


def _estilos():
    base = getSampleStyleSheet()
    estilos = {}

    estilos["titulo"] = ParagraphStyle(
        "titulo", parent=base["Normal"],
        fontSize=22, textColor=BLANCO, fontName="Helvetica-Bold",
        alignment=TA_LEFT, leading=28,
    )
    estilos["subtitulo"] = ParagraphStyle(
        "subtitulo", parent=base["Normal"],
        fontSize=11, textColor=AZUL_CLAR, fontName="Helvetica",
        alignment=TA_LEFT, leading=16,
    )
    estilos["seccion"] = ParagraphStyle(
        "seccion", parent=base["Normal"],
        fontSize=13, textColor=AZUL_OSC, fontName="Helvetica-Bold",
        alignment=TA_LEFT, leading=18, spaceBefore=6,
    )
    estilos["cuerpo"] = ParagraphStyle(
        "cuerpo", parent=base["Normal"],
        fontSize=9.5, textColor=NEGRO, fontName="Helvetica",
        alignment=TA_LEFT, leading=14,
    )
    estilos["kpi_valor"] = ParagraphStyle(
        "kpi_valor", parent=base["Normal"],
        fontSize=18, textColor=AZUL_OSC, fontName="Helvetica-Bold",
        alignment=TA_CENTER, leading=22,
    )
    estilos["kpi_label"] = ParagraphStyle(
        "kpi_label", parent=base["Normal"],
        fontSize=8, textColor=colors.HexColor("#555555"), fontName="Helvetica",
        alignment=TA_CENTER, leading=11,
    )
    estilos["tabla_header"] = ParagraphStyle(
        "tabla_header", parent=base["Normal"],
        fontSize=9, textColor=BLANCO, fontName="Helvetica-Bold",
        alignment=TA_CENTER,
    )
    estilos["pie"] = ParagraphStyle(
        "pie", parent=base["Normal"],
        fontSize=8, textColor=colors.HexColor("#888888"), fontName="Helvetica",
        alignment=TA_CENTER, leading=11,
    )
    return estilos


def _encabezado(story, e, metricas, nombre_empresa):
    """Banda de encabezado con fondo azul oscuro."""
    fecha = datetime.now().strftime("%B %Y").capitalize()

    header_data = [[
        Paragraph(f"{nombre_empresa}", e["titulo"]),
        Paragraph(f"Reporte de ventas<br/><font size='9'>{fecha}</font>", e["subtitulo"]),
    ]]
    t = Table(header_data, colWidths=[11*cm, 7*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), AZUL_OSC),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING",  (0,0), (0,0), 18),
        ("RIGHTPADDING", (1,0), (1,0), 18),
        ("TOPPADDING",   (0,0), (-1,-1), 16),
        ("BOTTOMPADDING",(0,0), (-1,-1), 16),
        ("ALIGN",        (1,0), (1,0), "RIGHT"),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.4*cm))


def _kpis(story, e, m):
    """Fila de 4 tarjetas KPI."""
    story.append(Paragraph("Resumen ejecutivo", e["seccion"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=AZUL_MED, spaceAfter=8))

    kpis = [
        (f"${m['ingreso_total']:,.0f}",  "Ingreso total anual"),
        (f"${m['ganancia_total']:,.0f}", "Ganancia total anual"),
        (f"{m['margen_promedio']}%",     "Margen promedio"),
        (f"{m['unidades_total']:,}",     "Unidades vendidas"),
    ]

    celdas = []
    for valor, label in kpis:
        celda = [
            Paragraph(valor, e["kpi_valor"]),
            Spacer(1, 2),
            Paragraph(label, e["kpi_label"]),
        ]
        celdas.append(celda)

    t = Table([celdas], colWidths=[4.5*cm]*4)
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), GRIS_CLAR),
        ("BOX",          (0,0), (-1,-1), 0.5, GRIS_MED),
        ("INNERGRID",    (0,0), (-1,-1), 0.5, GRIS_MED),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",   (0,0), (-1,-1), 12),
        ("BOTTOMPADDING",(0,0), (-1,-1), 12),
        ("ROUNDEDCORNERS", [4]),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))


def _highlights(story, e, m):
    """Tabla de highlights textuales."""
    story.append(Paragraph("Puntos destacados", e["seccion"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=AZUL_MED, spaceAfter=8))

    filas = [
        ["Indicador", "Resultado"],
        ["Producto más vendido (unidades)",
         f"{m['producto_top']}  ({m['unidades_top']:,} u.)"],
        ["Producto con mayor ingreso",
         f"{m['producto_mayor_ingreso']}  (${m['ingreso_mayor_producto']:,.2f})"],
        ["Categoría más rentable",    m["categoria_top"]],
        ["Mes con mayor facturación",
         f"{m['mes_top']}  (${m['ingreso_mes_top']:,.2f})"],
    ]

    t = Table(filas, colWidths=[8*cm, 10*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0),  AZUL_MED),
        ("TEXTCOLOR",    (0,0), (-1,0),  BLANCO),
        ("FONTNAME",     (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,0),  9),
        ("BACKGROUND",   (0,1), (-1,-1), BLANCO),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [BLANCO, GRIS_CLAR]),
        ("FONTNAME",     (0,1), (-1,-1), "Helvetica"),
        ("FONTSIZE",     (0,1), (-1,-1), 9),
        ("TEXTCOLOR",    (0,1), (-1,-1), NEGRO),
        ("FONTNAME",     (0,1), (0,-1),  "Helvetica-Bold"),
        ("TEXTCOLOR",    (0,1), (0,-1),  AZUL_OSC),
        ("ALIGN",        (0,0), (-1,-1), "LEFT"),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",   (0,0), (-1,-1), 7),
        ("BOTTOMPADDING",(0,0), (-1,-1), 7),
        ("LEFTPADDING",  (0,0), (-1,-1), 10),
        ("BOX",          (0,0), (-1,-1), 0.5, GRIS_MED),
        ("INNERGRID",    (0,0), (-1,-1), 0.3, GRIS_MED),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))


def _grafico(story, e, titulo, ruta, ancho=17*cm):
    story.append(Paragraph(titulo, e["seccion"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=AZUL_MED, spaceAfter=8))
    if os.path.exists(ruta):
        story.append(Image(ruta, width=ancho, height=ancho * 0.45))
    story.append(Spacer(1, 0.4*cm))


def _tabla_mensual(story, e, resumen_mensual):
    story.append(Paragraph("Detalle mensual", e["seccion"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=AZUL_MED, spaceAfter=8))

    filas = [["Mes", "Ingresos ($)", "Ganancias ($)", "Margen (%)"]]
    for _, row in resumen_mensual.iterrows():
        margen = (row["ganancia"] / row["ingreso"] * 100) if row["ingreso"] else 0
        filas.append([
            row["mes"],
            f"${row['ingreso']:,.2f}",
            f"${row['ganancia']:,.2f}",
            f"{margen:.1f}%",
        ])
    # Fila de totales
    tot_ing = resumen_mensual["ingreso"].sum()
    tot_gan = resumen_mensual["ganancia"].sum()
    tot_mar = (tot_gan / tot_ing * 100) if tot_ing else 0
    filas.append(["TOTAL", f"${tot_ing:,.2f}", f"${tot_gan:,.2f}", f"{tot_mar:.1f}%"])

    t = Table(filas, colWidths=[4.5*cm, 4.5*cm, 4.5*cm, 4.5*cm])
    last = len(filas) - 1
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0),      AZUL_MED),
        ("TEXTCOLOR",     (0,0), (-1,0),      BLANCO),
        ("FONTNAME",      (0,0), (-1,0),      "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,0),      9),
        ("BACKGROUND",    (0,1), (-1,last-1), BLANCO),
        ("ROWBACKGROUNDS",(0,1), (-1,last-1), [BLANCO, GRIS_CLAR]),
        ("BACKGROUND",    (0,last),(-1,last), colors.HexColor("#FFF2CC")),
        ("FONTNAME",      (0,last),(-1,last), "Helvetica-Bold"),
        ("TEXTCOLOR",     (0,last),(-1,last), colors.HexColor("#7F6000")),
        ("FONTNAME",      (0,1), (-1,last-1), "Helvetica"),
        ("FONTSIZE",      (0,1), (-1,last),   9),
        ("ALIGN",         (0,0), (-1,-1),     "CENTER"),
        ("VALIGN",        (0,0), (-1,-1),     "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1),     6),
        ("BOTTOMPADDING", (0,0), (-1,-1),     6),
        ("BOX",           (0,0), (-1,-1),     0.5, GRIS_MED),
        ("INNERGRID",     (0,0), (-1,-1),     0.3, GRIS_MED),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))


def _pie_pagina(story, e):
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GRIS_MED))
    story.append(Spacer(1, 0.2*cm))
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    story.append(Paragraph(
        f"Reporte generado automáticamente con Python  ·  {fecha}  ·  Confidencial",
        e["pie"]
    ))


def generar_pdf(metricas: dict, rutas_graficos: dict,
                nombre_empresa: str = "Ferretería Don José") -> str:

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, "reporte_ventas.pdf")

    doc = SimpleDocTemplate(
        path,
        pagesize=A4,
        leftMargin=1.8*cm, rightMargin=1.8*cm,
        topMargin=1.5*cm,  bottomMargin=1.5*cm,
    )

    e     = _estilos()
    story = []

    _encabezado(story, e, metricas, nombre_empresa)
    _kpis(story, e, metricas)
    _highlights(story, e, metricas)

    _grafico(story, e, "Ingresos y ganancias por mes",
             rutas_graficos.get("mensual", ""))

    _grafico(story, e, "Top 5 productos por ingreso",
             rutas_graficos.get("top5", ""))

    _tabla_mensual(story, e, metricas["resumen_mensual"])

    _grafico(story, e, "Participación de ingresos por categoría",
             rutas_graficos.get("categorias", ""), ancho=12*cm)

    _pie_pagina(story, e)

    doc.build(story)
    return path


if __name__ == "__main__":
    from lector import cargar_datos, calcular_metricas
    from graficos import generar_todos

    df      = cargar_datos("ventas_demo.xlsx")
    m       = calcular_metricas(df)
    graficos = generar_todos(m)
    ruta    = generar_pdf(m, graficos)
    print(f"  ✓ PDF generado → {ruta}")