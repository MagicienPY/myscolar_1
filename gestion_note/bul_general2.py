import pymysql
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

# Connexion à la base de données
conn = pymysql.connect(host='localhost', user='root', password='', db='g_note')
cursor = conn.cursor()

# Requête SQL pour récupérer les informations des étudiants
students_query = '''
SELECT DISTINCT etudiant.mat_etudiant, etudiant.nom_etu
FROM etudiant
'''

# Exécution de la requête pour récupérer les informations des étudiants
cursor.execute(students_query)
students = cursor.fetchall()

# Liste pour contenir les éléments de tous les bulletins
all_bulletin_elements = []

# Génération du bulletin individuel pour chaque étudiant
for student in students:
    mat_etudiant = student[0]
    nom_etudiant = student[1]

    # Requête SQL pour récupérer les données du bulletin de l'étudiant regroupées par semestre
    bulletin_query = f'''
    SELECT 
        note.semestre, 
        GROUP_CONCAT(DISTINCT CASE WHEN note.type_note = "examen" THEN matiere.nom_matiere END) as liste_matiere, 
        SUM(CASE WHEN note.type_note = "examen" THEN matiere.coef_matiere END) as somme_coefficients,
        etudiant.mat_etudiant, 
        etudiant.nom_etu, 
        note.type_note, 
        (SUM(note.note_cc * cote.cote_cc * matiere.coef_matiere) + SUM(note.note_sn * cote.cote_sn * matiere.coef_matiere)) / SUM(matiere.coef_matiere) AS moyenne, 
        RANK() OVER (PARTITION BY etudiant.mat_etudiant, note.semestre ORDER BY (SUM(note.note_cc * cote.cote_cc * matiere.coef_matiere) + SUM(note.note_sn * cote.cote_sn * matiere.coef_matiere)) / SUM(matiere.coef_matiere) DESC) AS ordre_merite
    FROM 
        cote 
    INNER JOIN 
        note ON cote.id_cote = note.id_cote 
    INNER JOIN 
        matiere ON note.id_matiere = matiere.id_matiere 
    INNER JOIN 
        etudiant ON etudiant.id_etudiant = note.id_etudiant 
    WHERE 
        note.type_note IN ("cc", "sn", "examen") AND etudiant.mat_etudiant = "{mat_etudiant}"
    GROUP BY 
        etudiant.mat_etudiant, note.semestre 
    ORDER BY 
        note.semestre, moyenne DESC
    '''

    # Exécution de la requête pour récupérer les données du bulletin de l'étudiant
    cursor.execute(bulletin_query)
    results = cursor.fetchall()

    # Liste pour contenir les éléments du bulletin de l'étudiant
    elements = []

    # Style des paragraphes
    styles = getSampleStyleSheet()
    style_title = styles['Title']
    style_heading = styles['Heading1']
    style_body = styles['BodyText']

    # Informations de l'étudiant
    title = Paragraph("Bulletin Universitaire", style_title)
    elements.append(title)

    elements.append(Spacer(1, 20))
    student_info = f"Nom de l'étudiant: {nom_etudiant}<br/>" \
                   f"Matricule de l'étudiant: {mat_etudiant}"
    student_info = Paragraph(student_info, style_body)
    elements.append(student_info)

    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Détails du bulletin:", style_heading))

    # Contenu du tableau
    data = [
        ["Semestre", "Liste des matières", "Somme des coefficients", "Moyenne", "Ordre de mérite"],
    ]

    for result in results:
        semestre = result[0]
        liste_matiere = result[1]
        somme_coefficients = result[2]
        moyenne = result[6]
        ordre_merite = result[7]

        data.append([semestre, liste_matiere, somme_coefficients, moyenne, ordre_merite])

    # Création du tableau avec le style
    table = Table(data)
    style = TableStyle([
        ('BACKGROUND', (0, 0),(-1, 0), colors.cyan),  # Couleur cyan pour les titres
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)

    elements.append(table)
    elements.append(Spacer(1, 20))

    # Ajout des éléments du bulletin de l'étudiant à la liste des bulletins généraux
    all_bulletin_elements.extend(elements)

# Fermeture de la connexion à la base de données
cursor.close()
conn.close()

# Création du document PDF avec tous les bulletins
doc = SimpleDocTemplate("bulletin_general.pdf", pagesize=landscape(letter))
doc.build(all_bulletin_elements)