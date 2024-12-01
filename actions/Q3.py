import tkinter as tk
from tkinter import ttk
from utils import display
from utils import db

class Window(tk.Toplevel):

    # Attributs de la classe (pour être en mesure de les utiliser dans les différentes méthodes)
    treeView = None
    input = None
    errorLabel = None

    def __init__(self, parent):
        super().__init__(parent)

        # Définition de la taille de la fenêtre et des lignes/colonnes
        display.centerWindow(600, 450, self)
        self.title('Q3 : nombre de mesures prises et moyenne des températures [...] (version dynamique)')
        display.defineGridDisplay(self, 3, 3)
        self.grid_rowconfigure(3, weight=10)  # Poids plus important pour afficher le tableau
        # Affichage du label, du Combobox et du bouton valider
        ttk.Label(self, text='Veuillez indiquer une région :', anchor="center", font=('Helvetica', '10', 'bold')).grid(row=1, column=0)

        # Création du Combobox pour la sélection dynamique de la région
        self.input = ttk.Combobox(self, state="readonly")
        self.input.grid(row=1, column=1)
        self.input.bind('<Return>', self.searchRegion)  # Bind Entrée
        ttk.Button(self, text='Valider', command=self.searchRegion).grid(row=1, column=2)

        # Affichage d'un label pour les erreurs
        self.errorLabel = ttk.Label(self, anchor="center", font=('Helvetica', '10', 'bold'))
        self.errorLabel.grid(columnspan=3, row=2, sticky="we")

        # Création d'un TreeView vide pour afficher les résultats
        columns = ('code_departement', 'nom_departement', 'num_mesures', 'moy_temp_moyenne')
        self.treeView = ttk.Treeview(self, columns=columns, show='headings')
        for column in columns:
            self.treeView.column(column, anchor=tk.CENTER, width=15)
            self.treeView.heading(column, text=column)
        self.treeView.grid(columnspan=3, row=3, sticky='nswe')

        # On remplit le Combobox avec les régions disponibles
        cursor = db.data.cursor()
        cursor.execute("SELECT DISTINCT nom_region FROM Regions")  # Récupère toutes les régions
        regions = cursor.fetchall()
        region_names = [region[0] for region in regions]
        self.input['values'] = region_names

    def searchRegion(self, event=None):
    # On vide le Treeview
        self.treeView.delete(*self.treeView.get_children())

    # On récupère la région sélectionnée
        region = self.input.get()

    # Si aucune région n'est sélectionnée, on affiche une erreur
        if len(region) == 0:
          self.errorLabel.config(foreground='red', text="Veuillez sélectionner une région !")
        else:
            try:
                cursor = db.data.cursor()
                result = cursor.execute("""
                SELECT d.code_departement, d.nom_departement, COUNT(m.code_departement) AS num_mesures, AVG(m.temperature_moy_mesure) AS moy_temp_moyenne
                FROM Departements d
                LEFT JOIN Mesures m ON d.code_departement = m.code_departement
                JOIN Regions r ON d.code_region = r.code_region
                WHERE r.nom_region = ?
                GROUP BY d.code_departement
                ORDER BY d.code_departement
            """, [region])

            except Exception as e:
            # Si une exception est levée, on l'affiche dans l'interface utilisateur
                self.errorLabel.config(foreground='red', text="Erreur : " + repr(e))
            else:
            # Si la requête s'est bien exécutée, on insère les résultats dans le Treeview
              i = 0
              for row in result:
                self.treeView.insert('', tk.END, values=row)
                i += 1

            # Message de retour en fonction du nombre de résultats
            if i == 0:
                self.errorLabel.config(foreground='orange', text="Aucun résultat pour la région \"" + region + "\" !")
            else:
                self.errorLabel.config(foreground='green', text="Voici les résultats pour la région \"" + region + "\" :")
