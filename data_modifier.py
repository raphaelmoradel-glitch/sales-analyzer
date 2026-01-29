import csv
import shutil
from data_loader import csv_to_dict, dict_to_csv

def afficher_ventes(data_dict):
    """
    Affiche toutes les ventes disponibles.

    Paramètres :
    -----------
    data_dict: dict
        dictionnaire du fichier csv

    Retourne :
    ---------
    str
        les ventes disponibles.
    """
    print("\nListe des ventes :")
    for i in range(len(data_dict['Order ID'])):
        print(f"\nVente {i + 1}:")
        for field in data_dict.keys():
            print(f"{field}: {data_dict[field][i]}")

def modifier_vente(file_path):
    """
    Modifie une entrée existante dans un fichier CSV.

    Paramètres :
    -----------
    file_path : str
        Chemin d'accès du fichier CSV.
    """
    data_dict = csv_to_dict(file_path)
    afficher_ventes(data_dict)
    try:
        choix = int(input("\nEntrez le numéro de la vente à modifier : ")) - 1
        if choix < 0 or choix >= len(data_dict['Order ID']):
            print("Numéro invalide.")
            return
        
    except ValueError:
        print("Veuillez entrer un numéro valide.")
        return
    print("\nDétails actuels de la vente :")
    for field in data_dict.keys():
        print(f"{field}: {data_dict[field][choix]}")

    print("\nChamps disponibles pour modification :")
    champs = list(data_dict.keys())
    for i, field in enumerate(champs, start=1):
        print(f"{i}. {field}")
    
    try:
        champ_choisi = int(input("\nEntrez le numéro du champ à modifier : ")) - 1
        if champ_choisi < 0 or champ_choisi >= len(champs):
            print("Numéro invalide.")
            return
    except ValueError:
        print("Veuillez entrer un numéro valide.")
        return
    
    nouvelle_valeur = input(f"Entrez la nouvelle valeur pour '{champs[champ_choisi]}' : ")
    
    data_dict[champs[champ_choisi]][choix] = nouvelle_valeur
    
    print("\nModification à appliquer :")
    print(f"{champs[champ_choisi]}: {nouvelle_valeur}")
    confirmation = input("Voulez-vous sauvegarder cette modification ? (o/n) : ").strip().lower()
    
    if confirmation == 'o':
        dict_to_csv(file_path, data_dict)
        print("\nModification sauvegardée avec succès !")
    else:
        print("\nModification annulée.")

def ajouter_vente(file_path):
    """
    Ajoute une nouvelle entrée dans le fichier CSV.

    Paramètres :
    -----------
    file_path : str
        Chemin d'accès du fichier CSV.

    Retourne :
    ---------
    str
        Fichier CSV modifier avec la vente ajouté
    """
    data_dict = csv_to_dict(file_path)
    
    nouvelle_vente = {}
    for field in data_dict.keys():
        nouvelle_vente[field] = input(f"Entrez la valeur pour '{field}' : ")
    
    print("\nNouvelle vente à ajouter :")
    for field, value in nouvelle_vente.items():
        print(f"{field}: {value}")
    
    confirmation = input("Voulez-vous sauvegarder cette nouvelle vente ? (o/n) : ").strip().lower()
    
    if confirmation == 'o':
        for field, value in nouvelle_vente.items():
            data_dict[field].append(value)
        
        dict_to_csv(file_path, data_dict)
        print("\nNouvelle vente ajoutée avec succès !")
    else:
        print("\nAjout annulé.")