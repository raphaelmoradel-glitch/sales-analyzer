from datetime import datetime
import csv

def filter_by_date(data, search_date):
    """
    Filtre les ventes selon une date donnée.

    Paramètres :
    - data (dict) : Dictionnaire contenant les ventes.
    - search_date (str) : Date au format "MM/JJ/AA".

    Retourne :
    - list : Liste des ventes correspondant à cette date.
    """
    result = []

    for i in range(len(data["Order Date"])):
        order_date = data["Order Date"][i]

        try:
            order_datetime = datetime.strptime(order_date, "%m/%d/%y %H:%M")
            formatted_order_date = order_datetime.strftime("%m/%d/%y") 

            if formatted_order_date == search_date:
                result.append({
                    "Order ID": data["Order ID"][i],
                    "Product": data["Product"][i],
                    "Quantity Ordered": data["Quantity Ordered"][i],
                    "Price Each": data["Price Each"][i],
                    "Order Date": order_date,
                    "Purchase Address": data["Purchase Address"][i]
                })
        
        except ValueError:
            continue
    
    return result

def filter_by_product(data, product_name):
    """
    Filtre les ventes pour un produit spécifique.

    Paramètres :
    - data (dict) : Dictionnaire contenant les ventes.
    - product_name (str) : Nom du produit recherché.

    Retourne :
    - list : Liste des ventes correspondant au produit.
    """
    result = []

    for i in range(len(data["Product"])):
        if data["Product"][i].strip().lower() == product_name.strip().lower():
            result.append({
                "Order ID": data["Order ID"][i],
                "Product": data["Product"][i],
                "Quantity Ordered": data["Quantity Ordered"][i],
                "Price Each": data["Price Each"][i],
                "Order Date": data["Order Date"][i],
                "Purchase Address": data["Purchase Address"][i]
            })

    return result

def get_user_input(prompt, convert_type):
    """
    Fonction pour récupérer et convertir une entrée utilisateur.

    Paramètres :
    - prompt (str) : Message affiché à l'utilisateur.
    - convert_type (type) : Type de conversion (int, float).

    Retourne :
    - La valeur convertie ou None si l'utilisateur ne renseigne rien.
    """
    value = input(prompt)
    return convert_type(value) if value.strip() else None

def filter_by_quantity_or_price(data, min_q, max_q, min_p, max_p):
    """
    Filtre les ventes selon des seuils minimums et/ou maximums de quantités vendues ou de prix.
    """

    result = []

    for i in range(len(data["Order ID"])):
        try:
            quantity = int(data["Quantity Ordered"][i])
            price = float(data["Price Each"][i]) 

            if ((min_q is None or quantity >= min_q) and
                (max_q is None or quantity <= max_q) and
                (min_p is None or price >= min_p) and
                (max_p is None or price <= max_p)):

                result.append({
                    "Order ID": data["Order ID"][i],
                    "Product": data["Product"][i],
                    "Quantity Ordered": quantity,
                    "Price Each": price,
                    "Order Date": data["Order Date"][i],
                    "Purchase Address": data["Purchase Address"][i]
                })
        
        except ValueError:
            continue

    return result

def most_and_least_sold_products(data):
    """
    Trouve le produit le plus vendu et le moins vendu.

    Paramètres :
    - data (dict) : Dictionnaire contenant les ventes (issu de csv_to_dict).

    Retourne :
    - tuple : (produit le plus vendu, quantité), (produit le moins vendu, quantité)
    """
    sales_count = {}

    for i in range(len(data["Product"])):
        product = data["Product"][i]
        quantity_str = data["Quantity Ordered"][i].strip()

        if quantity_str.isdigit(): 
            quantity = int(quantity_str)
            if product in sales_count:
                sales_count[product] += quantity
            else:
                sales_count[product] = quantity

    if not sales_count:
        return None, None
    
    most_sold = max(sales_count.items(), key=lambda x: x[1])
    least_sold = min(sales_count.items(), key=lambda x: x[1])

    return most_sold, least_sold
