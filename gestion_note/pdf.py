import aspose.pdf as pdf
from aspose import *


def pdfp ():
            # Créer un nouveau document PDF
    doc = pdf.Document()

            # Ajouter une page
    page = doc.pages.add()

            # Récupérer le contexte graphique de la page  
    gfx = pdf.Graphics(page)

            # Imprimer du texte
    gfx.DrawString("Bonjour je suis le magicien", pdf.Font(pdf.FontFamily.HELVETICA, 20), pdf.Brushes.Black, 100, 100)

            # Imprimer des données issues d'une variable
    nom = "Marc"
    gfx.DrawString(nom, pdf.Font(pdf.FontFamily.HELVETICA, 20), pdf.Brushes.Black, 100, 150) 

            # Imprimer une liste
    liste = ["Item 1", "Item 2", "Item 3"]
    for i, item in enumerate(liste):
        gfx.DrawString(item, pdf.Font(pdf.FontFamily.HELVETICA, 12), pdf.Brushes.Black, 100, 200+i*20)

            # Enregistrer le document
        doc.Save("document.pdf")
##################################################################
pdfp()