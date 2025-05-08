from fpdf import FPDF


def generarpdf(datos, reporte):
    if not datos:
        print("No hay datos para generar el PDF.")
        return

    pdf = FPDF()
    pdf.add_page()

    # Título del reporte
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, txt="Reporte de Datos", ln=True, align="C")
    pdf.ln(10)  # espacio

    pdf.set_font("Arial", size=12)

    # Encabezado dinámico
    claves = list(datos[0].keys())
    encabezado = " | ".join(claves)
    pdf.cell(200, 10, txt=encabezado, ln=True)

    # Línea por línea de datos
    for item in datos:
        # Verifica si necesita agregar nueva página
        if pdf.get_y() > 270:
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=encabezado, ln=True)

        linea = " | ".join(str(item.get(clave, "")) for clave in claves)
        pdf.cell(200, 10, txt=linea, ln=True)

    pdf.output(reporte)
