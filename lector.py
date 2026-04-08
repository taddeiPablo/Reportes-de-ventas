import pandas as pd


COSTOS_UNITARIOS = {
    "Tornillos 6x1 (caja x100)": 0.45,
    "Pintura látex blanca 4L":   9.80,
    "Llave combinada 13mm":      5.50,
    "Cinta métrica 5m":          3.20,
    "Taladro percutor 650W":    52.00,
    "Tubo PVC 110mm x 6m":      11.50,
    "Lija al agua grano 120":    0.60,
    "Cerradura doble paleta":   17.00,
}


def cargar_datos(path: str) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="Ventas", header=3)
    df.columns = ["mes", "producto", "categoria", "unidades", "precio_unit", "ingreso", "costo", "ganancia"]
    df = df[df["mes"].notna() & (df["mes"] != "TOTAL GENERAL")].copy()
    df["unidades"]    = pd.to_numeric(df["unidades"],    errors="coerce")
    df["precio_unit"] = pd.to_numeric(df["precio_unit"], errors="coerce")
    df["ingreso"]     = df["unidades"] * df["precio_unit"]
    df["costo"]       = df["producto"].map(COSTOS_UNITARIOS) * df["unidades"]
    df["ganancia"]    = df["ingreso"] - df["costo"]
    return df


def calcular_metricas(df: pd.DataFrame) -> dict:
    orden_meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
                   "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

    # Totales generales
    ingreso_total  = df["ingreso"].sum()
    ganancia_total = df["ganancia"].sum()
    unidades_total = int(df["unidades"].sum())
    margen_prom    = (ganancia_total / ingreso_total * 100) if ingreso_total else 0

    # Producto más vendido (por unidades)
    por_producto = df.groupby("producto")["unidades"].sum()
    producto_top = por_producto.idxmax()
    unidades_top = int(por_producto.max())

    # Producto con mayor ingreso
    por_ingreso = df.groupby("producto")["ingreso"].sum()
    producto_mayor_ingreso = por_ingreso.idxmax()
    ingreso_mayor          = por_ingreso.max()

    # Categoría más rentable
    por_cat = df.groupby("categoria")["ganancia"].sum()
    categoria_top = por_cat.idxmax()

    # Mes con mayor ingreso
    por_mes = df.groupby("mes")["ingreso"].sum()
    mes_top = por_mes.idxmax()
    ingreso_mes_top = por_mes.max()

    # Resumen mensual ordenado (para gráfico)
    resumen_mensual = (
        df.groupby("mes")[["ingreso", "ganancia"]]
        .sum()
        .reindex([m for m in orden_meses if m in df["mes"].unique()])
        .reset_index()
    )

    # Resumen por categoría (para gráfico de torta)
    resumen_categoria = (
        df.groupby("categoria")["ingreso"]
        .sum()
        .reset_index()
        .sort_values("ingreso", ascending=False)
    )

    # Top 5 productos por ingreso
    top5_productos = (
        df.groupby("producto")["ingreso"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    return {
        "ingreso_total":           round(ingreso_total, 2),
        "ganancia_total":          round(ganancia_total, 2),
        "unidades_total":          unidades_total,
        "margen_promedio":         round(margen_prom, 1),
        "producto_top":            producto_top,
        "unidades_top":            unidades_top,
        "producto_mayor_ingreso":  producto_mayor_ingreso,
        "ingreso_mayor_producto":  round(ingreso_mayor, 2),
        "categoria_top":           categoria_top,
        "mes_top":                 mes_top,
        "ingreso_mes_top":         round(ingreso_mes_top, 2),
        "resumen_mensual":         resumen_mensual,
        "resumen_categoria":       resumen_categoria,
        "top5_productos":          top5_productos,
    }


if __name__ == "__main__":
    df = cargar_datos("ventas_demo.xlsx")
    m  = calcular_metricas(df)

    print("=" * 50)
    print("  MÉTRICAS CALCULADAS — Ferretería Don José")
    print("=" * 50)
    print(f"  Ingreso total:        $ {m['ingreso_total']:,.2f}")
    print(f"  Ganancia total:       $ {m['ganancia_total']:,.2f}")
    print(f"  Unidades vendidas:      {m['unidades_total']:,}")
    print(f"  Margen promedio:        {m['margen_promedio']} %")
    print(f"  Producto más vendido:   {m['producto_top']} ({m['unidades_top']:,} u.)")
    print(f"  Mayor ingreso producto: {m['producto_mayor_ingreso']}")
    print(f"  Categoría más rentable: {m['categoria_top']}")
    print(f"  Mes estrella:           {m['mes_top']}  ($ {m['ingreso_mes_top']:,.2f})")
    print()
    print("  Resumen mensual:")
    print(m["resumen_mensual"].to_string(index=False))
    print()
    print("  Top 5 productos por ingreso:")
    print(m["top5_productos"].to_string(index=False))