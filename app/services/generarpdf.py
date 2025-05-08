from fpdf import FPDF

def generatorpdf(data, keys, name, title="Reporte de Datos"):
    pdf = FPDF()
    pdf.add_page()

    # Título del reporte 
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, txt=title, ln=True, align="C")

    # Encabezados de columnas
    pdf.set_font("Arial", style="B", size=12)
    encabezado = " | ".join(keys)
    pdf.cell(200, 10, txt=encabezado, ln=True)

    # Contenido de los datos
    pdf.set_font("Arial", size=12)
    for item in data:
        linea = " | ".join(str(item.get(clave, "")) for clave in keys)
        pdf.cell(200, 10, txt=linea, ln=True)

    # Guardar el archivo PDF
    pdf.output(name)