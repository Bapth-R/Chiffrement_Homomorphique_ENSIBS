import sqlite3
import sys, os,json
sys.path.append('libs')
sys.path.append(os.getcwd())

PATH_CONFIG = "Config/config.json"
configuration = json.loads(open(PATH_CONFIG,"r").read())

DATABASE = configuration["NAME_DATABASE"]
TABLE_Q31 = configuration["NAME_TABLE"]
VERBOSE = configuration["VERBOSE"]

# Connect to the database
cnx = sqlite3.connect(DATABASE)

# Create a cursor to execute SQL statements
cursor = cnx.cursor()


def check_item_exist(table:str, item_name:str, verbose:bool=False):
    """
    Vérifie si un élément existe dans la table
    :param table: nom de la table
    :param item_name: nom de l'élément à vérifier
    :param verbose: mode verbeux
    :return: True si l'élément existe, False sinon
    """
    # Create a cursor object to execute SQL queries

    # Execute a SELECT query to check if the item exists
    query = "SELECT * FROM %s WHERE items='%s' ;"%(table, item_name) 
    cursor.execute(query)

    # If the query returns a result, the item exists
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False
    
def check_table_in_database(table_name):
    """
    Vérifie si une table existe dans la base de données
    :param table_name: nom de la table à vérifier
    :return: True si la table existe, False sinon
    """
    # Create a cursor object to execute SQL queries

    # Execute a SHOW TABLES query to get a list of tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';",)

    # Iterate over the tables and check if the given table name exists
    tables = [table[0] for table in cursor]
    if table_name in tables:
        return True
    else:
        return False

def create_database(database_name:str, verbose:bool=False):
    """
    Vérifie si une table existe dans la base de données
    :param table_name: nom de la table à vérifier
    :return: True si la table existe, False sinon
    """
    query = "CREATE DATABASE %s"%database_name
    cursor.execute(query)
   
    results = cnx.commit()

    return results


def create_table(table:str, items:list,verbose:bool=False):
    """
    Crée une table
    :param table: nom de la table à créer
    :param items: liste de tuples contenant le nom et le type de chaque colonne de la table
    :param verbose: mode verbeux
    :return: None
    """
    if check_table_in_database(table):
        return False
    query = "CREATE TABLE %s (" %(table) + ",".join(["%s %s" % (name, type) for name, type in items]) + ")"
    cursor.execute(query)
   
    results = cursor.fetchall()

    # Print the results
    return [row for row in results]

def list_item_in_bdd(table:str, verbose:bool=False):
    """
    Liste les éléments de la table
    :param table: nom de la table
    :param verbose: mode verbeux
    :return: liste des éléments de la table
    """
    query = "SELECT * FROM (%s) "%(table)
    cursor.execute(query)
    results = cursor.fetchall()

    # Print the results
    return [row for row in results]

def add_item_in_bdd(table:str, items:list, verbose:bool=False):
    """
    Ajoute un nouvel enregistrement dans la table spécifiée avec les items fournis.

    Args:
        table (str): Nom de la table dans laquelle l'enregistrement sera ajouté.
        items (list): Liste des items de l'enregistrement, sous forme de paires (nom, valeur).
                      La valeur peut être de type str ou int.
        verbose (bool, optionnel): Si True, affiche un message pour confirmer que l'enregistrement a été ajouté avec succès.

    Returns:
        bool: True si l'enregistrement a été ajouté avec succès, False sinon.
    """
    if check_item_exist(table, items[0][1]):
        return False
    
    query = "INSERT INTO %s "%(table) + "(" +",".join([" %s " % (name)  for name,_ in items]) + ") VALUES (" +",".join([" '%s' " % (ii) for _,ii in items]) + ");"
    cursor.execute(query)
   
    results = cnx.commit()
    
    return results

def get_value(table:str, items, value_type, verbose:bool=False):
    """
    Cette fonction récupère les valeurs de la table selon le type de valeur spécifié.

    Args:
        table (str): Nom de la table
        items (list): Liste des éléments
        value_type (str): Type de valeur à récupérer (PHE ou OPE)
        verbose (bool, optional): Si True, affiche des informations supplémentaires. Defaults to False.

    Returns:
        results: Résultats de la requête SQL.
    """
    

    for item in items:
        if value_type.lower() == "ope":
            if "*" in str(items):
                query = "SELECT nombre_ope FROM %s;"%(table) 
            else:
                query = "SELECT nombre_ope FROM %s WHERE items='%s' ;"%(table, item) 
        else:
            if "*" in str(items):
                query = "SELECT nombre_phe, exposant_phe FROM %s ;"%(table) 
            else:
                query = "SELECT nombre_phe, exposant_phe FROM %s WHERE items='%s' ;"%(table, item)
        cursor.execute(query)

        results = cursor.fetchall()
        
    return results

def list_table(table:str, verbose:bool=False):
    """
    Cette fonction renvoie la liste des noms de colonnes de la table.

    Args:
        table (str): Nom de la table
        verbose (bool, optional): Si True, affiche des informations supplémentaires. Defaults to False.

    Returns:
        List: Liste des noms de colonnes de la table.
    """
    query = "PRAGMA table_info('%s');"%(table)
    cursor.execute(query)
   
    results = cursor.fetchall()

    # Print the results
    return [row for row in results]

if __name__ == "__main__":
   pass