import tkinter as tk
from utils import display, db
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        display.centerWindow(1500, 800, self)
        self.title('Comparaison des records de températures - Zone H1 en 2018')
        display.defineGridDisplay(self, 1, 1)

        # Requête SQL pour récupérer les données nécessaires
        query = """
            WITH TempH1 AS (
                SELECT M.date_mesure, M.temperature_moy_mesure, D.zone_climatique
                FROM Mesures M
                JOIN Departements D ON M.code_departement = D.code_departement
                WHERE D.zone_climatique = 'H1' AND strftime('%Y', M.date_mesure) = '2018'
            ),
            Records AS (
                SELECT 
                    date_mesure,
                    MIN(temperature_moy_mesure) AS record_froid,
                    MAX(temperature_moy_mesure) AS record_chaud
                FROM Mesures
                GROUP BY date_mesure
            )
            SELECT 
                R.date_mesure,
                R.record_froid,
                R.record_chaud,
                MIN(T.temperature_moy_mesure) AS temp_min_zone_h1,
                MAX(T.temperature_moy_mesure) AS temp_max_zone_h1
            FROM Records R
            JOIN TempH1 T ON R.date_mesure = T.date_mesure
            GROUP BY R.date_mesure
        """

        result = []
        try:
            cursor = db.data.cursor()
            result = cursor.execute(query)
        except Exception as e:
            print("Erreur : " + repr(e))

        # Extraction et préparation des valeurs pour le graphique
        dates, record_froid, record_chaud, temp_min_h1, temp_max_h1 = [], [], [], [], []
        for row in result:
            dates.append(row[0])
            record_froid.append(row[1])
            record_chaud.append(row[2])
            temp_min_h1.append(row[3])
            temp_max_h1.append(row[4])

        # Formatage des dates pour l'affichage sur l'axe x
        datetime_dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]

        # Configuration du graphique
        fig = Figure(figsize=(15, 8), dpi=100)
        plot1 = fig.add_subplot(111)

        # Tracé des courbes
        plot1.plot(datetime_dates, record_froid, color='blue', label='Record de fraîcheur')
        plot1.plot(datetime_dates, record_chaud, color='red', label='Record de chaleur')
        plot1.plot(datetime_dates, temp_min_h1, color='cyan', label='Température min zone H1 (2018)')
        plot1.plot(datetime_dates, temp_max_h1, color='orange', label='Température max zone H1 (2018)')

        # Configuration des labels et de la légende
        plot1.set_xticks(datetime_dates[::30])  # Affiche une date par mois
        plot1.set_xticklabels([date.strftime('%b') for date in datetime_dates[::30]], rotation=45)
        plot1.legend()

        # Affichage du graphique dans la fenêtre Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

