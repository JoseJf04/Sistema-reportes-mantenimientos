"""Clase PDF para generar documentos de reportes"""

from fpdf import FPDF

class PDF(FPDF):
    def __init__(self):
        super().__init__(orientation='L', format=(216, 330))

    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Datos de reportes", 0, 1, "C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Pagina {self.page_no()}", 0, 0, "C")
    
    def crear_tabla(self, encabezamiento, datos, ancho_de_columnas):
        # Encabezamiento
        self.set_font("Arial", "B", 10)
        for i in range(len(encabezamiento)):
            self.cell(ancho_de_columnas[i], 10, encabezamiento[i], 1, 0, "C")
        self.ln()
        
        # Datos
        self.set_font("Arial", "", 10)
        for fila in datos:
            for i in range(len(fila)):
                self.cell(ancho_de_columnas[i], 10, str(fila[i]), 1, 0, "C")
            self.ln()