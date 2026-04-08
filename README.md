# 📊 Generador automático de reportes de ventas

Herramienta en Python que lee un archivo Excel con datos de ventas, calcula métricas clave, genera gráficos y produce un **reporte PDF profesional** listo para descargar — todo en menos de 2 segundos.

> Desarrollado como demostración de automatización para PyMEs con Python.

---

## 🎯 ¿Qué problema resuelve?

Muchas PyMEs llevan sus ventas en Excel pero pierden horas cada mes armando reportes a mano: copiar datos, hacer gráficos, calcular totales, formatear el documento.

Este script hace todo eso automáticamente con un solo comando.

**Antes:** 2 a 3 horas de trabajo manual por mes  
**Después:** `python main.py` → reporte listo en 2 segundos

---

## 📁 Estructura del proyecto

```
reporte-ventas/
│
├── ventas_demo.xlsx      ← datos de ejemplo (Ferretería Don José)
├── lector.py             ← lectura y cálculo de métricas con pandas
├── graficos.py           ← generación de gráficos con matplotlib
├── reporte.py            ← armado del PDF con reportlab
├── emailer.py            ← envío automático por email (opcional)
├── main.py               ← punto de entrada principal
├── .env.example          ← plantilla de variables de entorno
└── output/               ← carpeta generada automáticamente
    ├── grafico_mensual.png
    ├── grafico_top5.png
    ├── grafico_categorias.png
    └── reporte_ventas.pdf
```

---

## 🚀 Instalación y uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/reporte-ventas.git
cd reporte-ventas
```

### 2. Instalar dependencias

```bash
pip install pandas openpyxl matplotlib reportlab python-dotenv
```

### 3. Ejecutar con los datos de demo

```bash
python main.py
```

### 4. Ejecutar con tu propio Excel

```bash
python main.py mis_ventas.xlsx
```

El archivo Excel debe tener las columnas: `Mes`, `Producto`, `Categoría`, `Unidades vendidas`, `Precio unit. ($)`.

---

## 📄 ¿Qué contiene el reporte PDF?

- **Encabezado** con nombre del negocio y fecha de generación
- **4 KPIs** — ingreso total, ganancia total, margen promedio, unidades vendidas
- **Puntos destacados** — producto estrella, mes pico, categoría más rentable
- **Gráfico de barras** — ingresos y ganancias por mes
- **Gráfico horizontal** — top 5 productos por ingreso
- **Tabla mensual** — detalle de los 12 meses con margen por mes
- **Gráfico de torta** — participación de ingresos por categoría

---

## 📧 Envío automático por email (opcional)

Para activar el envío automático del PDF por email, copiá `.env.example` a `.env` y completá tus datos:

```bash
cp .env.example .env
```

```env
EMAIL_REMITENTE=tuemail@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop
REPORTE_EMAIL=destinatario@gmail.com
```

> ⚠️ `EMAIL_PASSWORD` no es tu contraseña de Gmail sino una **contraseña de aplicación**.  
> Podés generarla en: Google Account → Seguridad → Contraseñas de aplicaciones.

Una vez configurado, el email se envía automáticamente al correr `python main.py`.

---

## 🛠️ Tecnologías utilizadas

| Librería | Uso |
|---|---|
| `pandas` | Lectura y procesamiento del Excel |
| `openpyxl` | Creación del archivo Excel de demo |
| `matplotlib` | Generación de gráficos |
| `reportlab` | Construcción del PDF |
| `smtplib` | Envío por email (stdlib de Python) |
| `python-dotenv` | Manejo de credenciales |

---

## 🔧 Personalización

Para adaptar el script a otro negocio editás dos cosas:

**1. Los costos unitarios en `lector.py`:**
```python
COSTOS_UNITARIOS = {
    "Tu producto A": 10.50,
    "Tu producto B": 25.00,
}
```

**2. El nombre del negocio en `main.py`:**
```python
ruta_pdf = generar_pdf(metricas, rutas_graficos, nombre_empresa="Tu Negocio")
```

---

## 👨‍💻 Autor

Desarrollado por **Pablo Taddei**  
Fullstack Developer — Python · .NET · Angular · Flutter  
[LinkedIn](https://linkedin.com/in/tu-perfil) · [Portfolio](https://tu-portfolio.com)

---

## 📬 ¿Necesitás algo similar para tu negocio?

Puedo adaptar esta herramienta a tus datos, tu formato y tus procesos.  
Escribime por LinkedIn o al correo **taddeiapablo23@gmail.com**

---

> *Este proyecto es parte de mi portfolio de automatizaciones con Python para PyMEs.*
