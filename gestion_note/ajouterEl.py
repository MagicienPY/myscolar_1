import customtkinter as ctk
import mysql.connector
from subprocess import call
from tkinter import messagebox
import pymysql
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from departement2 import *

import sqlite3
import pymysql
class ajouterEl:
    def __init__(self):
        pass
    def ajoue (self):
        global essaie
        essaie = 0

        #dep = Vue()


        def fermer ():
            ajouterEl.destroy()
        def tentative ():
            global essaie
            essaie += 1
            lable1 = ctk.CTkLabel(master= ajouterEl, text = "nombre de tentative restante  "+str(essaie),bg_color="red")
            lable1.pack(padx= 1, pady= 0)

            
            #messagebox.showinfo("nombre de tentative restante",essaie)
            if essaie==3:
                messagebox.showinfo("Attention","vous n'avez plus d'autre tentative !")
                ajouterEl.destroy()
        def creatione():
        # mysqldb = mysql.connector.connect(host="localhost", user="root", password="",database="gestage")
        # mycursor = mysqldb.cursor()
            try:
                con = pymysql.connect(user='root', password ='',database = 'g_note')
                cursor = con.cursor()
                print("connecté avec succes")
                iden = id_etudiant.get()
                mat_e = mat_etudiant.get()
                cin_et = cin_etudiant.get()
                daten = daten_etu.get()
                lieun = lieun_etu.get()
                add = adress_etu.get()
                tel =  tel_etu.get()
                nom = nom_etu.get()
                prenom = prenom_etu.get()

                print(prenom)
                command="use g_note"
                cursor.execute(command)
                sql = "INSERT INTO etudiant (id_etudiant, mat_etudiant, cin_etudiant, daten_etu, lieun_etu, adress_etu, tel_etu, nom_etu, prenom_etu) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)"
                cursor.execute(sql, (iden, mat_e, cin_et, daten, lieun, add, tel, nom, prenom))
                con.commit()
                messagebox.showinfo(" cool ", "enregistrement reussit !!")
                ajouterEl.destroy()
            except:
                messagebox.showinfo("attention", "un soucis veuillez verifier vos informations")



        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")


        ajouterEl = ctk.CTk()
        ajouterEl.title("MYSCOLAR")
        ajouterEl.geometry("900x700")

        #une frame au centre

        frame = ctk.CTkFrame(master= ajouterEl)
        frame.pack(padx = 220, pady = 60, fill= "both", expand = True) 

        frame3 = ctk.CTkFrame(master= ajouterEl,width=200,height=300)
        frame3.place(x = 0, y = 60) 


        #label
        print("ajoue d'etudiant")
        lable = ctk.CTkLabel(master= frame, text = "Ajoue d'Etudiant")
        lable.pack(padx= 12, pady= 10)




        id_etudiant = ctk.CTkEntry(master=  frame, placeholder_text="identifiant")
        id_etudiant.pack(padx= 12)

        mat_etudiant = ctk.CTkEntry(master=  frame, placeholder_text="mat_etudiant")
        mat_etudiant.pack(padx= 12)


        cin_etudiant = ctk.CTkEntry(master=  frame, placeholder_text="cin_etudiant")
        cin_etudiant.pack(padx= 12)

        daten_etu = ctk.CTkEntry(master=  frame, placeholder_text="daten_etu")
        daten_etu.pack(pady= 12)

        lieun_etu = ctk.CTkEntry(master=  frame, placeholder_text="lieun_etu")
        lieun_etu.pack(padx= 12)

        adress_etu = ctk.CTkEntry(master=  frame, placeholder_text="adress_etu")
        adress_etu.pack(padx= 12)

        tel_etu = ctk.CTkEntry(master=  frame, placeholder_text="tel_etu")
        tel_etu.pack(padx= 12)


        nom_etu = ctk.CTkEntry(master=  frame, placeholder_text="nom_etu")
        nom_etu.pack(padx= 12)

        prenom_etu = ctk.CTkEntry(master=  frame, placeholder_text="prenom_etu")
        prenom_etu.pack(pady= 12)


        button = ctk.CTkButton(master=frame, text="Ajouter",command=creatione)
        button.pack(padx=10, pady=12)

        button = ctk.CTkButton(master=frame3, text="Annuler",command=fermer)
        button.pack(padx=10, pady=12)

        #ajouterEl.mainloop()