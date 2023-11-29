import customtkinter as ctk
import mysql.connector
from subprocess import call
from tkinter import messagebox
import pymysql
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from departement2 import *
from chefdep import *
from agent import *

import sqlite3
import pymysql

global essaie
essaie = 0

#dep = Vue()


def fermer ():
    authen.destroy()
def tentative ():
    global essaie
    essaie += 1
    lable1 = ctk.CTkLabel(master= authen, text = "nombre de tentative restante  "+str(essaie),bg_color="red")
    lable1.pack(padx= 1, pady= 0)

    
    #messagebox.showinfo("nombre de tentative restante",essaie)
    if essaie==3:
        messagebox.showinfo("Attention","vous n'avez plus d'autre tentative !")
        authen.destroy()
def authenticate_user():
    con = pymysql.connect(user='root', password ='',database = 'g_note')
    cursor = con.cursor()
    username = chama.get()
    password = chama2.get()

    # Requête SQL pour vérifier les informations d'identification
    query = """
            SELECT r.nom_role 
            FROM role r
            inner JOIN utilisateur u ON u.role_id = r.id
            WHERE u.nom = %s AND u.password = %s
            """
    values = (username, password)
    cursor.execute(query, values)
    result = cursor.fetchone()
    print(result)

    if result is not None:
        role = result[0]
        if role == "admin":
            # Rediriger vers la page d'administration
            messagebox.showinfo("Connexion réussie", "Bienvenue, Admin!")
            authen.destroy()
            ri = Vueri()

            ri.acceuil()
        elif role == "chef_dep":
            # Rediriger vers la page du chef de département
            messagebox.showinfo("Connexion réussie", "Bienvenue, Chef de département!")
            authen.destroy()
            cp = chef_dep()
            cp.acceuil()
        elif role == "agent":
            # Rediriger vers la page de l'agent
            messagebox.showinfo("Connexion réussie", "Bienvenue, Agent!")
            authen.destroy()
            cp = agent()
            cp.acceuil()
    else:
        # Afficher un message d'erreur si les informations d'identification sont incorrectes
        messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect.")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


authen = ctk.CTk()
authen.title("AUTH-SERCU")
authen.geometry("900x700")

#une frame au centre

frame = ctk.CTkFrame(master= authen)
frame.pack(padx = 220, pady = 60, fill= "both", expand = True) 

frame3 = ctk.CTkFrame(master= authen,width=200,height=300)
frame3.place(x = 0, y = 60) 


#label

lable = ctk.CTkLabel(master= frame, text = "se connecter")
lable.pack(padx= 12, pady= 10)

lable = ctk.CTkLabel(master= frame3, text = "   Bonjour et bienvenue sur AUTH SECUR    ", bg_color="cyan",height=65,width=70, text_color="black")
lable.pack(padx= 30, pady= 30)


chama = ctk.CTkEntry(master=  frame, placeholder_text="IDENTIFIANT", show= "+")
chama.pack(padx= 12)

chama2 = ctk.CTkEntry(master=  frame, placeholder_text="mot de passe", show="*-")
chama2.pack(pady= 12)


button = ctk.CTkButton(master=frame, text="connection",command=authenticate_user)
button.pack(padx=10, pady=12)

button = ctk.CTkButton(master=frame3, text="Annuler",command=fermer)
button.pack(padx=10, pady=12)

authen.mainloop()