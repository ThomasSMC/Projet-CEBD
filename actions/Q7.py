import tkinter as tk
from utils import display
from tkinter import ttk
from utils.db import data

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre, du titre et des lignes/colonnes de l'affichage grid
        display.centerWindow(800, 600, self)
        self.title('Q7 : gérer les travaux de rénovation')
        display.defineGridDisplay(self, 4, 2)

        self.modification_en_cours = False  # Pour bloquer tout autre action si on veut modifier

        """ttk.Label(self,
                  text="Proposer des fonctionnalités permettant de gérer l'ajout, modification et suppression pour un "
                       "type de travaux",
                  wraplength=500,
                  anchor="center",
                  font=('Helvetica', '10', 'bold')
                  ).grid(sticky="we", row=0)"""

        self.liste_travaux = ttk.Treeview(self, columns=('departement', 'travaux'), show='headings', height=20)
        self.liste_travaux.heading('departement', text="Département")
        self.liste_travaux.heading('travaux', text="Travaux")
        self.liste_travaux.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Menu déroulant département
        ttk.Label(self, text="Département :").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.dep_combobox = ttk.Combobox(self, state="readonly")
        self.dep_combobox.grid(row=2, column=1, padx=10, pady=5)
        self.chercher_departements()

        # Menu déroulant travaux
        ttk.Label(self, text="Travaux :").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.travaux_combobox = ttk.Combobox(self, state="readonly")
        self.travaux_combobox.grid(row=3, column=1, padx=10, pady=5)
        self.travaux_combobox['values'] = ["Isolation", "Chauffage", "Photovoltaïque"]

        # Boutons
        ttk.Button(self, text="Ajouter", command=self.ajouter).grid(row=4, column=0, pady=5, sticky="w", padx=10)
        ttk.Button(self, text="Modifier", command=self.modifier).grid(row=4, column=1, pady=5)
        ttk.Button(self, text="Supprimer", command=self.supprimer).grid(row=4, column=2, pady=5, sticky="e", padx=10)

        # On récupère le contenu de la base de donnée
        self.actualiser_tableau()

    def chercher_departements(self):
        try:
            cursor = data.cursor()
            cursor.execute("SELECT nom_departement FROM Departements")
            departements = [dep[0] for dep in cursor.fetchall()]
            self.dep_combobox['values'] = departements
        except Exception as e:
            print(f"Erreur lors de la récupération des départements : {e}")

    def actualiser_tableau(self):
        for item in self.liste_travaux.get_children():
            self.liste_travaux.delete(item)
        try:
            cursor = data.cursor()
            cursor.execute("SELECT departement, travaux FROM Travaux")
            for row in cursor.fetchall():
                self.liste_travaux.insert("", "end", values=row)
        except Exception as e:
            print(f"Erreur lors de la récupération des informations : {e}")

    def ajouter(self):
        if not self.modification_en_cours:
            # Ajouter un travail à un département
            departement = self.dep_combobox.get()
            travaux = self.travaux_combobox.get()
            if departement and travaux:
                cursor = data.cursor()
                cursor.execute("SELECT COUNT(*) FROM Travaux WHERE departement = ? AND travaux = ?", (departement, travaux))
                count = cursor.fetchone()[0]
                if count == 0:
                    # L'entrée n'existe pas
                    cursor.execute("INSERT INTO Travaux (departement, travaux) VALUES (?, ?)", (departement, travaux))
                    data.commit()
                    self.actualiser_tableau()
                else:
                    print(f"Lex travaux '{travaux}' existe déjà pour le département '{departement}'.")

    def supprimer(self):
        if not self.modification_en_cours:
            departement = self.dep_combobox.get()
            travaux = self.travaux_combobox.get()
            if departement and travaux:
                cursor = data.cursor()
                cursor.execute("SELECT COUNT(*) FROM Travaux WHERE departement = ? AND travaux = ?", (departement, travaux))
                count = cursor.fetchone()[0]
                if count != 0:
                    # Il y a une occurence
                    cursor.execute("DELETE FROM Travaux WHERE departement = ? AND travaux = ?", (departement, travaux))
                    data.commit()
                    self.actualiser_tableau()
                    print(f"Travaux supprimés : {departement}, {travaux}")
                else:
                    print(f"Les travaux n'existent pas : {departement}, {travaux}")

    def modifier(self):
        self.modification_en_cours = True
        departement = self.dep_combobox.get()
        travaux = self.travaux_combobox.get()

        if departement and travaux:
            # On vérifie si on peut modifier
            cursor = data.cursor()
            cursor.execute("SELECT COUNT(*) FROM Travaux WHERE departement = ? AND travaux = ?", (departement, travaux))
            count = cursor.fetchone()[0]
            if count != 0:
                # Alors on peut modifier la ligne
                # Masquage du premier menu déroulant des travaux
                self.travaux_combobox.grid_forget()

                # Menu déroulant avec les travaux restant possibles
                autres_travaux = [t for t in ["Isolation", "Chauffage", "Photovoltaïque"] if t != travaux]
                self.travaux_modif_combobox = ttk.Combobox(self, values=autres_travaux, state="readonly")
                self.travaux_modif_combobox.grid(row=3, column=1, padx=10, pady=5)

                # Le bouton modifier devient valider
                self.bouton_valider = ttk.Button(self, text="Valider", command=lambda:self.valider_modification(departement, travaux))
                self.bouton_valider.grid(row=4, column=1, pady=5)
            else:
                print(f"Les travaux ne peuvent pas être modifiés car ils n'existent pas : {departement}, {travaux}")

    def valider_modification(self, departement, anciens_travaux):
        nouveau_travaux = self.travaux_modif_combobox.get()

        if nouveau_travaux:
            cursor = data.cursor()
            cursor.execute("SELECT COUNT(*) FROM Travaux WHERE departement = ? AND travaux = ?", (departement, nouveau_travaux))
            count = cursor.fetchone()[0]
            if count == 0:
                cursor.execute("UPDATE Travaux SET travaux = ? WHERE departement = ? AND travaux = ?",
                               (nouveau_travaux, departement, anciens_travaux))
                data.commit()
                self.actualiser_tableau()
                print(
                    f"Travaux modifiés : {departement} -> {anciens_travaux} => {departement} -> {nouveau_travaux}")
            else:
                print(f"Les travaux : {departement}, {anciens_travaux} ne peuvent pas être modifiés en {departement}, "
                      f"{nouveau_travaux} car ces derniers existent déjà dans la table")


        # On remet le bouton modifier
        self.travaux_modif_combobox.grid_forget()
        self.bouton_valider.grid_forget()

        # On remet le menu déroulant complet
        self.travaux_combobox.grid(row=3, column=1, padx=10, pady=5)

        self.modification_en_cours = False  # On a finit de modifier