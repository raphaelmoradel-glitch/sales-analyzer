import csv
from data_loader import csv_to_dict, dict_to_csv
from data_modifier import afficher_ventes, modifier_vente, ajouter_vente
from filters import filter_by_date, filter_by_product, filter_by_quantity_or_price, most_and_least_sold_products, get_user_input
from statistics import calculate_total_revenue, identifier_date_ventes_max, calculer_ventes_et_revenus, trier_produits, afficher_resultats

def afficher_menu():
    """
    Affiche le menu principal avec les options disponibles.
    """
    print("\n========Menu ESME market======== :")
    print("1. Afficher les ventes pour une date donnée")
    print("2. Afficher les ventes pour un produit spécifique")
    print("3. Filtrer les ventes par quantité ou prix")
    print("4. Trouver le produit le plus vendu et le produit le moins vendu")
    print("5. Calculer un chiffre d'affaires total")
    print("6. Identifier la date avec les ventes les plus élevées")
    print("7. Trier les produits par ventes ou revenus")
    print("8. Ajouter une vouvelle vente ou modifier une entrée existante")
    print("9. Quitter")
    print()

def menu_interactif():
    """
    Gère l'interaction avec l'utilisateur pour choisir et exécuter les actions.
    """
    file_path = "C:\APP1\Sales_April_2019.csv" 
    csv_data = csv_to_dict(file_path)
    
    while True:
        afficher_menu()
        choix = input("Choisissez une option (1-9) : ")
        
        if choix == "1":
            date_input = input("Entrez une date au format MM/JJ/AA : ")
            ventes = filter_by_date(csv_data, date_input)
            if ventes:
                print("\n📅 Ventes du", date_input)
                for vente in ventes:
                    print(vente)
            else:
                print("\n❌ Aucune vente trouvée pour cette date.")

        elif choix == "2":
            produit_recherche = input("Entrez le nom du produit : ")
            ventes = filter_by_product(csv_data, produit_recherche)
            if ventes:
                for vente in ventes:
                    print(vente)
            else:
                print("\n❌ Aucune vente trouvée pour ce produit.")

        elif choix == "3":
            min_q = get_user_input("Entrez la quantité minimale (laisser vide pour ignorer) : ", int)
            max_q = get_user_input("Entrez la quantité maximale (laisser vide pour ignorer) : ", int)
            min_p = get_user_input("Entrez le prix minimum (laisser vide pour ignorer) : ", float)
            max_p = get_user_input("Entrez le prix maximum (laisser vide pour ignorer) : ", float)
            filtered_sales = filter_by_quantity_or_price(csv_data, min_q, max_q, min_p, max_p)
            if filtered_sales:
                for sale in filtered_sales:
                    print(sale)
            else:
                print("\n❌ Aucune vente trouvée avec ces critères.")
        
        elif choix == "4":
            most_sold, least_sold = most_and_least_sold_products(csv_data)
            if most_sold and least_sold:
                print(f"📈 Produit le plus vendu : {most_sold[0]} avec {most_sold[1]} ventes")
                print(f"📉 Produit le moins vendu : {least_sold[0]} avec {least_sold[1]} ventes")
            else:
                print("⚠️ Aucune donnée valide trouvée dans le fichier CSV.")

        elif choix == "5":
            start_date = input("Entrez la date de début (format MM/DD/YY, ou laissez vide pour aucune période) : ")
            end_date = input("Entrez la date de fin (format MM/DD/YY, ou laissez vide pour aucune période) : ")
            product = input("Entrez le nom du produit (ou laissez vide pour tous les produits) : ")
            total_revenue = calculate_total_revenue(file_path, start_date, end_date, product)
            if start_date and end_date:
                print(f"Le chiffre d'affaires total pour '{product if product else 'tous les produits'}' entre {start_date} et {end_date} est: ${total_revenue:.2f}")
            else:
                print(f"Le chiffre d'affaires total pour '{product if product else 'tous les produits'}' est: ${total_revenue:.2f}")

        elif choix == "6":
            dates_max, chiffre_affaires_max = identifier_date_ventes_max(file_path)
            if len(dates_max) == 1:
                print(f"La date avec les ventes les plus élevées est le {dates_max[0].strftime('%d/%m/%Y')} avec un chiffre d'affaires de : ${chiffre_affaires_max:.2f}")
            else:
                print(f"Les dates avec les ventes les plus élevées sont : {', '.join([date.strftime('%d/%m/%Y') for date in dates_max])} avec un chiffre d'affaires de : ${chiffre_affaires_max:.2f}")
        
        elif choix == "7":
            data_dict = csv_to_dict(file_path)
            produits = calculer_ventes_et_revenus(data_dict)
            critere = input("Voulez-vous trier par 'ventes' ou 'revenus' ? ").strip().lower()
            try:
                produits_tries = trier_produits(produits, critere)
            except ValueError as e:
                print(e)
                return
            afficher_resultats(produits_tries, critere)
        
        elif choix == "8":
            while True:
                print("\n--- Menu Principal ---")
                print("1. Modifier une vente existante")
                print("2. Ajouter une nouvelle vente")
                print("3. Retour")
        
                choix = input("Choisissez une option (1-3) : ")
        
                if choix == '1':
                    modifier_vente(file_path)
                elif choix == '2':
                    ajouter_vente(file_path)
                elif choix == '3':
                    break
                else:
                    print("Option invalide. Veuillez choisir une option entre 1 et 3.")
        
        elif choix == "9":
            print("Au revoir!")
            break
        
        else:
            print("Choix invalide, essayez à nouveau.")

if __name__ == "__main__":
    menu_interactif()
        
       
