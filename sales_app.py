import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from data_loader import csv_to_dict, dict_to_csv
from data_modifier import afficher_ventes, modifier_vente, ajouter_vente
from filters import filter_by_date, filter_by_product, filter_by_quantity_or_price, most_and_least_sold_products
from statistics import calculate_total_revenue, identifier_date_ventes_max, calculer_ventes_et_revenus, trier_produits, afficher_resultats
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from collections import defaultdict

# Chemin du fichier CSV
FILE_PATH = "C:/APP1/Sales_April_2019.csv"

class SalesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Ventes")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")  # Couleur de fond

        # Charger les données du CSV
        self.data_dict = csv_to_dict(FILE_PATH)

        # Créer l'interface utilisateur
        self.create_widgets()

    def create_widgets(self):
        # Titre
        title_label = tk.Label(
            self.root,
            text="Gestion des Ventes",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#333333",
        )
        title_label.pack(pady=20)

        # Cadre pour les boutons
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=10)

        # Boutons pour les fonctionnalités
        buttons = [
            ("1. Afficher les ventes pour une date donnée", self.show_sales_by_date),
            ("2. Afficher les ventes pour un produit spécifique", self.show_sales_by_product),
            ("3. Filtrer les ventes par quantité ou prix", self.filter_sales),
            ("4. Trouver le produit le plus vendu et le moins vendu", self.show_most_and_least_sold),
            ("5. Calculer un chiffre d'affaires total", self.calculate_total_revenue),
            ("6. Identifier la date avec les ventes les plus élevées", self.show_max_sales_date),
            ("7. Trier les produits par ventes ou revenus", self.sort_products),
            ("8. Ajouter une nouvelle vente ou modifier une entrée existante", self.add_or_modify_sale),
            ("9. Visualiser les ventes par produit", self.plot_sales_by_product),
            ("10. Visualiser l'évolution des ventes par mois", self.plot_sales_by_month),
            ("11. Quitter", self.quit_app),
        ]

        for text, command in buttons:
            button = tk.Button(
                button_frame,
                text=text,
                command=command,
                width=60,
                font=("Arial", 12),
                bg="#4CAF50",  # Couleur de fond
                fg="white",    # Couleur du texte
                activebackground="#45a049",  # Couleur au clic
                relief=tk.FLAT,  # Bordure plate
            )
            button.pack(pady=5, padx=10)

    def show_sales_by_date(self):
        date = simpledialog.askstring("Date", "Entrez une date (MM/JJ/AA) :")
        if date:
            sales = filter_by_date(self.data_dict, date)
            self.display_results(sales, f"Ventes du {date}")

    def show_sales_by_product(self):
        product = simpledialog.askstring("Produit", "Entrez le nom du produit :")
        if product:
            sales = filter_by_product(self.data_dict, product)
            self.display_results(sales, f"Ventes pour {product}")

    def filter_sales(self):
        # Demander les seuils à l'utilisateur
        min_q = self.get_user_input("Entrez la quantité minimale (laisser vide pour ignorer) : ", int)
        max_q = self.get_user_input("Entrez la quantité maximale (laisser vide pour ignorer) : ", int)
        min_p = self.get_user_input("Entrez le prix minimum (laisser vide pour ignorer) : ", float)
        max_p = self.get_user_input("Entrez le prix maximum (laisser vide pour ignorer) : ", float)

        # Filtrer les ventes
        filtered_sales = filter_by_quantity_or_price(self.data_dict, min_q, max_q, min_p, max_p)

        # Afficher les résultats
        if filtered_sales:
            self.display_results(filtered_sales, "Ventes filtrées")
        else:
            messagebox.showinfo("Aucun résultat", "❌ Aucune vente trouvée avec ces critères.")

    def get_user_input(self, prompt, convert_type):
        """
        Demande à l'utilisateur de saisir une valeur et la convertit.
        Si l'utilisateur laisse le champ vide, retourne None.
        """
        value = simpledialog.askstring("Filtre", prompt)
        if value and value.strip():
            try:
                return convert_type(value)
            except ValueError:
                messagebox.showerror("Erreur", f"Valeur invalide : {value}")
                return None
        return None

    def show_most_and_least_sold(self):
        most_sold, least_sold = most_and_least_sold_products(self.data_dict)
        if most_sold and least_sold:
            messagebox.showinfo(
                "Produits les plus et moins vendus",
                f"Produit le plus vendu : {most_sold[0]} ({most_sold[1]} ventes)\n"
                f"Produit le moins vendu : {least_sold[0]} ({least_sold[1]} ventes)",
            )
        else:
            messagebox.showinfo("Erreur", "Aucune donnée valide trouvée.")

    def calculate_total_revenue(self):
        start_date = simpledialog.askstring("Date de début", "Entrez la date de début (MM/JJ/AA) :")
        end_date = simpledialog.askstring("Date de fin", "Entrez la date de fin (MM/JJ/AA) :")
        product = simpledialog.askstring("Produit", "Entrez le nom du produit (optionnel) :")
        total_revenue = calculate_total_revenue(FILE_PATH, start_date, end_date, product)
        messagebox.showinfo("Chiffre d'affaires total", f"Chiffre d'affaires total : ${total_revenue:.2f}")

    def show_max_sales_date(self):
        dates_max, chiffre_affaires_max = identifier_date_ventes_max(FILE_PATH)
        if len(dates_max) == 1:
            messagebox.showinfo(
                "Date avec ventes max",
                f"Date : {dates_max[0].strftime('%d/%m/%Y')}\nChiffre d'affaires : ${chiffre_affaires_max:.2f}",
            )
        else:
            dates_str = ", ".join([date.strftime('%d/%m/%Y') for date in dates_max])
            messagebox.showinfo(
                "Dates avec ventes max",
                f"Dates : {dates_str}\nChiffre d'affaires : ${chiffre_affaires_max:.2f}",
            )

    def sort_products(self):
        produits = calculer_ventes_et_revenus(self.data_dict)
        critere = simpledialog.askstring("Critère de tri", "Voulez-vous trier par 'ventes' ou 'revenus' ?")
        if critere:
            try:
                produits_tries = trier_produits(produits, critere)
                self.display_results(produits_tries, f"Produits triés par {critere}")
            except ValueError as e:
                messagebox.showerror("Erreur", str(e))

    def add_or_modify_sale(self):
        # Sous-menu pour ajouter ou modifier une vente
        choix = simpledialog.askinteger(
            "Ajouter ou modifier une vente",
            "Choisissez une option :\n1. Ajouter une nouvelle vente\n2. Modifier une vente existante",
        )
        if choix == 1:
            ajouter_vente(FILE_PATH)
            self.data_dict = csv_to_dict(FILE_PATH)  # Recharger les données
        elif choix == 2:
            modifier_vente(FILE_PATH)
            self.data_dict = csv_to_dict(FILE_PATH)  # Recharger les données
        else:
            messagebox.showinfo("Erreur", "Option invalide.")

    def plot_sales_by_product(self):
        # Calculer les ventes par produit
        produits = calculer_ventes_et_revenus(self.data_dict)
        produits_tries = sorted(produits.items(), key=lambda x: x[1]['quantite'], reverse=True)

        # Extraire les noms des produits et les quantités vendues
        produits_noms = [p[0] for p in produits_tries]
        quantites = [p[1]['quantite'] for p in produits_tries]

        # Créer un graphique en barres
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(produits_noms, quantites, color='skyblue')
        ax.set_title("Ventes par produit")
        ax.set_xlabel("Produit")
        ax.set_ylabel("Quantité vendue")
        plt.xticks(rotation=45, ha='right')

        # Afficher le graphique dans une nouvelle fenêtre
        self.display_plot(fig)

    def plot_sales_by_month(self):
        """
        Génère un graphique en ligne et un tableau montrant l'évolution des ventes par mois.
        """
        # Extraire les dates et les quantités vendues
        dates = []
        quantites = []
        for date_str, quantite_str in zip(self.data_dict['Order Date'], self.data_dict['Quantity Ordered']):
        # Ignorer les dates ou quantités vides
            if not date_str or not quantite_str:
                print(f"Ignorer la ligne avec une date ou quantité vide : {date_str}, {quantite_str}")
                continue  # Passer à la ligne suivante

            try:
                # Convertir la date en objet datetime
                date = datetime.strptime(date_str, "%m/%d/%y %H:%M")
                # Convertir la quantité en entier
                quantite = int(quantite_str)
                dates.append(date)
                quantites.append(quantite)
            except ValueError as e:
                print(f"Ignorer la ligne avec une date ou quantité invalide : {date_str}, {quantite_str}")
                continue  # Passer à la ligne suivante

        # Trouver la plage de dates complète
        if not dates:
            messagebox.showinfo("Aucune donnée", "Aucune donnée valide trouvée.")
            return

        # Déterminer le premier et le dernier mois
        min_date = min(dates)
        max_date = max(dates)

        # Générer tous les mois entre le premier et le dernier mois
        current_date = datetime(min_date.year, min_date.month, 1)
        end_date = datetime(max_date.year, max_date.month, 1)
        all_months = []
        while current_date <= end_date:
            all_months.append(current_date.strftime("%Y-%m"))
            # Passer au mois suivant
            if current_date.month == 12:
                current_date = datetime(current_date.year + 1, 1, 1)
            else:
                current_date = datetime(current_date.year, current_date.month + 1, 1)

        # Grouper les ventes par mois
        ventes_par_mois = defaultdict(int)
        for date, quantite in zip(dates, quantites):
            mois = date.strftime("%Y-%m")  # Formater la date en "AAAA-MM"
            ventes_par_mois[mois] += quantite

        # Remplir les mois sans ventes avec 0
        ventes_completes = {mois: ventes_par_mois.get(mois, 0) for mois in all_months}

        # Trier les mois
        mois_tries = sorted(ventes_completes.keys())
        quantites_triees = [ventes_completes[mois] for mois in mois_tries]

        # Créer un graphique en ligne
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(mois_tries, quantites_triees, marker='o', color='orange', linestyle='-')
        ax.set_title("Évolution des ventes par mois")
        ax.set_xlabel("Mois")
        ax.set_ylabel("Quantité vendue")
        plt.xticks(rotation=45, ha='right')  # Rotation des étiquettes de l'axe X pour une meilleure lisibilité

        # Afficher le graphique dans une nouvelle fenêtre
        self.display_plot(fig)

        # Afficher les données dans un tableau
        tableau_data = [{"Mois": mois, "Quantité vendue": quantite} for mois, quantite in ventes_completes.items()]
        self.display_results(tableau_data, "Ventes par mois")

    def display_plot(self, fig):
        """
        Affiche un graphique Matplotlib dans une nouvelle fenêtre Tkinter.
        """
        # Créer une nouvelle fenêtre pour afficher le graphique
        plot_window = tk.Toplevel(self.root)
        plot_window.title("Graphique")
        plot_window.geometry("800x600")

        # Intégrer le graphique dans la fenêtre Tkinter
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)

    def display_results(self, results, title):
        """
        Affiche les résultats dans un tableau.
        """
        # Créer une nouvelle fenêtre pour afficher les résultats
        result_window = tk.Toplevel(self.root)
        result_window.title(title)
        result_window.geometry("1000x600")

        # Créer un Treeview pour afficher les résultats sous forme de tableau
        tree = ttk.Treeview(result_window, columns=list(results[0].keys()), show="headings")
        tree.pack(expand=True, fill=tk.BOTH)

        # Configurer les colonnes
        for col in results[0].keys():
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor=tk.CENTER)

        # Ajouter les données au Treeview
        for result in results:
            tree.insert("", tk.END, values=list(result.values()))

        # Ajouter une barre de défilement
        scrollbar = ttk.Scrollbar(result_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bouton pour fermer la fenêtre
        close_button = tk.Button(result_window, text="Fermer", command=result_window.destroy)
        close_button.pack(pady=10)

    def quit_app(self):
        if messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter ?"):
            self.root.quit()

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = SalesApp(root)
    root.mainloop()