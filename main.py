import sys
import os
import time
from dotenv import load_dotenv
from lector import cargar_datos, calcular_metricas
from graficos import generar_todos
from reporte import generar_pdf

load_dotenv()


def log(mensaje: str):
    print(f"  {mensaje}")


def main():
    print()
    print("=" * 52)
    print("   Generador de reportes de ventas — Don José")
    print("=" * 52)

    # ── 1. Archivo Excel ─────────────────────────────────
    excel_path = sys.argv[1] if len(sys.argv) > 1 else "data/ventas_demo.xlsx"

    if not os.path.exists(excel_path):
        print(f"\n  ERROR: No se encontró el archivo '{excel_path}'")
        print("  Uso: python main.py [archivo.xlsx]\n")
        sys.exit(1)

    # ── 2. Lectura y métricas ────────────────────────────
    log("Leyendo datos del Excel...")
    t0 = time.time()
    df       = cargar_datos(excel_path)
    metricas = calcular_metricas(df)
    log(f"✓ {len(df)} registros procesados  ({time.time()-t0:.2f}s)")

    print()
    print("  ── Métricas principales ──────────────────────")
    log(f"Ingreso total:     $ {metricas['ingreso_total']:>12,.2f}")
    log(f"Ganancia total:    $ {metricas['ganancia_total']:>12,.2f}")
    log(f"Margen promedio:     {metricas['margen_promedio']:>11.1f} %")
    log(f"Unidades vendidas:   {metricas['unidades_total']:>12,}")
    log(f"Producto estrella:   {metricas['producto_top']}")
    log(f"Mes más fuerte:      {metricas['mes_top']}")
    print("  ──────────────────────────────────────────────")
    print()

    # ── 3. Gráficos ──────────────────────────────────────
    log("Generando gráficos...")
    t0 = time.time()
    rutas_graficos = generar_todos(metricas)
    for nombre, ruta in rutas_graficos.items():
        log(f"  ✓ {nombre:12} → {ruta}")
    log(f"Gráficos listos  ({time.time()-t0:.2f}s)")
    print()

    # ── 4. PDF ───────────────────────────────────────────
    log("Generando PDF...")
    t0 = time.time()
    ruta_pdf = generar_pdf(metricas, rutas_graficos)
    tam_kb   = os.path.getsize(ruta_pdf) / 1024
    log(f"✓ PDF listo → {ruta_pdf}  ({tam_kb:.0f} KB)  ({time.time()-t0:.2f}s)")
    print()

    # ── 5. Email opcional ────────────────────────────────
    destinatario = os.environ.get("REPORTE_EMAIL")
    if destinatario:
        log(f"Enviando reporte a {destinatario}...")
        try:
            from emailer import enviar_reporte
            enviar_reporte(destinatario, ruta_pdf)
            log(f"✓ Email enviado a {destinatario}")
        except Exception as err:
            log(f"✗ No se pudo enviar el email: {err}")
        print()

    print("=" * 52)
    print("   ¡Reporte generado con éxito!")
    print(f"   Abrí el archivo: {ruta_pdf}")
    print("=" * 52)
    print()


if __name__ == "__main__":
    main()