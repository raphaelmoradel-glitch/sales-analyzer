import csv
from datetime import datetime
from collections import defaultdict

def calculate_total_revenue(file_path, start_date=None, end_date=None, product=None):
    """
    Calcule le revenu total à partir d'un fichier CSV contenant des commandes.

    paramètres:
        file_path (str): Chemin du fichier CSV contenant les données de commande.
        start_date (str, optional): Date de début pour filtrer les commandes, au format "MM/JJ/AA".
        end_date (str, optional): Date de fin pour filtrer les commandes, au format "MM/JJ/AA".
        product (str, optional): Nom du produit à filtrer. Si spécifié, seules les commandes de ce produit seront prises en compte.

    Retourne:
        float: Le revenu total calculé en fonction des critères de filtrage.
    """
    total_revenue = 0.0
    
    if start_date:
        start_date = datetime.strptime(start_date, "%m/%d/%y") 
    if end_date:
        end_date = datetime.strptime(end_date, "%m/%d/%y")
    
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            if not row['Order Date'] or (product and not row['Product']):
                continue 
            
            # convertir order date en datetime objet
            try:
                order_date = datetime.strptime(row['Order Date'], "%m/%d/%y %H:%M") 
            except ValueError:
                print(f"Passer le tour car format invalide: {row['Order Date']}")
                continue  
            if start_date and end_date:
                if not (start_date <= order_date <= end_date):
                    continue  
            
            if product and row['Product'] != product:
                continue  
            
            quantity = int(row['Quantity Ordered'])
            unit_price = float(row['Price Each'])
            total_revenue += quantity * unit_price
                
    return total_revenue

def identifier_date_ventes_max(file_path):
    """
    Identifie la ou les dates avec le chiffre d'affaires maximal à partir d'un fichier CSV contenant des commandes.

    Paramètres:
        file_path (str): Chemin du fichier CSV contenant les données de commande.

    Retourne:
        tuple: Une liste des dates (datetime.date) où le chiffre d'affaires était maximal, 
               et la valeur du chiffre d'affaires maximal (float).

    Le fichier CSV doit contenir les colonnes suivantes :
        - 'Order Date' (format "MM/JJ/AA HH:MM")
        - 'Quantity Ordered'
        - 'Price Each'

    Les lignes avec des formats de date invalides ou des valeurs manquantes pour 'Order Date' sont ignorées.
    """
    chiffre_affaires_par_date = defaultdict(float)
    
    with open(file_path, mode='r') as file:
        lecteur_csv = csv.DictReader(file)
        
        for ligne in lecteur_csv:
            if not ligne['Order Date']:
                continue
            
            try:
                date_commande = datetime.strptime(ligne['Order Date'], "%m/%d/%y %H:%M")
            except ValueError:
                print(f"Ignorer la ligne en raison d'un format de date invalide : {ligne['Order Date']}")
                continue
            
            date_sans_heure = date_commande.date()
            quantite = int(ligne['Quantity Ordered'])
            prix_unitaire = float(ligne['Price Each'])
            chiffre_affaires_par_date[date_sans_heure] += quantite * prix_unitaire
    
    chiffre_affaires_max = max(chiffre_affaires_par_date.values())
    
    dates_max = [date for date, ca in chiffre_affaires_par_date.items() if ca == chiffre_affaires_max]
    
    return dates_max, chiffre_affaires_max

def calculer_ventes_et_revenus(data_dict):
    """
    Calcule les ventes (quantité vendue) et les revenus (chiffre d'affaires) pour chaque produit.
    
    Paramètres :
    - data_dict (dict) : Dictionnaire contenant les données du CSV.

    Retourne :
    - dict : Un dictionnaire où chaque clé est un produit, et chaque valeur est un dictionnaire
             contenant la quantité vendue et les revenus.
    """
    produits = {}
    for i in range(len(data_dict['Product'])):
        if not data_dict['Quantity Ordered'][i] or not data_dict['Price Each'][i]:
            continue
        
        try:
            produit = data_dict['Product'][i]
            quantite = int(data_dict['Quantity Ordered'][i])
            prix_unitaire = float(data_dict['Price Each'][i])
        except ValueError as e:
            print(f"Ignorer la ligne {i + 1} en raison d'une valeur invalide : {e}")
            continue
        
        if produit not in produits:
            produits[produit] = {'quantite': 0, 'revenus': 0.0}
        
        produits[produit]['quantite'] += quantite
        produits[produit]['revenus'] += quantite * prix_unitaire
    
    return produits

def trier_produits(produits, critere='ventes'):
    """
    Trie les produits par ventes (quantité) ou par revenus (chiffre d'affaires).
    
    Paramètres :
    - produits (dict) : Dictionnaire contenant les données des produits.
    - critere (str) : Critère de tri ('ventes' ou 'revenus').

    Retourne :
    - list : Une liste de tuples (produit, données) triée selon le critère.
    """
    if critere == 'ventes':
        # Trier par quantité vendue (décroissant)
        return sorted(produits.items(), key=lambda x: x[1]['quantite'], reverse=True)
    elif critere == 'revenus':
        # Trier par revenus (décroissant)
        return sorted(produits.items(), key=lambda x: x[1]['revenus'], reverse=True)
    else:
        raise ValueError("Critère de tri invalide. Choisissez 'ventes' ou 'revenus'.")

def afficher_resultats(produits_tries, critere):
    """
    Affiche les produits triés par ventes ou revenus.
    
    Paramètres :
    - produits_tries (list) : Liste de tuples (produit, données) triée.
    - critere (str) : Critère de tri utilisé.

    Retourne :
    - list : Une liste de tuples (produit, données) triée selon le critère.
    """
    print(f"\nProduits triés par {critere} :")
    for produit, donnees in produits_tries:
        if critere == 'ventes':
            print(f"{produit}: {donnees['quantite']} unités vendues")
        elif critere == 'revenus':
            print(f"{produit}: ${donnees['revenus']:.2f} de revenus")