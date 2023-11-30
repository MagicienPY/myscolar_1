from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from tkinter import Tk
from tkinter import messagebox
import pymysql

con76 = pymysql.connect(user='root', password='', database='g_note')
cursor = con76.cursor()

query = 'select * from matiere;'
r = cursor.execute(query)
data = cursor.fetchall()

con76.close()

# Créez un document PDF
pdf_filename = 'table2.pdf'
document = SimpleDocTemplate(pdf_filename, pagesize=letter)

# Créez un tableau avec les données
table_data = [["identifiant", "Nom matiere", "id_module", "coef"]] # En-têtes de colonnes
table_data += data

table = Table(table_data)

# Appliquez un style au tableau
style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
])

table.setStyle(style)

# Ajoutez le tableau au document PDF
elements = [table]
document.build(elements)

# Affichez un message de confirmation
Tk().withdraw()  # masquer la fenêtre racine Tkinter
messagebox.showinfo("PDF créé", "Le PDF du tableau a été créé avec succès.")