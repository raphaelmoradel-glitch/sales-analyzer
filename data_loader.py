import csv

def csv_to_dict(file_path):
    """
    Charge les données commerciales depuis un fichier CSV et les organise dans un dictionnaire.
    Chaque colonne devient une clé, et les valeurs sont stockées dans une liste.
    
    Paramètres :
    -----------
    file_path : str
        Chemin d'accès du fichier CSV.

    Retourne :
    ---------
    dict
        Dictionnaire avec les données organisées par colonnes.
    """
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data_dict = {field: [] for field in reader.fieldnames}
        for row in reader:
            for field in reader.fieldnames:
                data_dict[field].append(row[field])
    return data_dict

def dict_to_csv(file_path, data_dict):
    """
    Convertit un dictionnaire de listes en un fichier CSV.
    
    Paramètres :
    - file_path (str) : Chemin du fichier CSV.
    - data_dict (dict) : Dictionnaire où chaque clé correspond à une colonne du CSV,
                         et chaque valeur est une liste contenant les valeurs de cette colonne.

    Retourne :
    csv
        Fichier CSV avec les valeur d'un dictionnaire.
    """
    with open(file_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data_dict.keys())
        writer.writeheader()
        for i in range(len(next(iter(data_dict.values())))):
            row = {field: data_dict[field][i] for field in data_dict.keys()}
            writer.writerow(row)
            

