# Côté client
import sys
sys.path.append('libs')

import socket
import pickle
import json

PATH_CONFIG = "Config/config.json"
configuration = json.loads(open(PATH_CONFIG,"r").read())

PORT  = configuration["PORT_SOCKET"]
DATABASE = configuration["NAME_DATABASE"]
TABLE_Q31 = configuration["NAME_TABLE"]
VERBOSE = configuration["VERBOSE"]

def header():
    print("""\n\n\n\t\033[91m_______________________________________________________________

\t   _____ ______________  ______  ______   ____  ____  ____ 
\t  / ___// ____/ ____/ / / / __ \/ ____/  / __ )/ __ \/ __ \\
\t  \__ \/ __/ / /   / / / / /_/ / __/    / __  / / / / / / /
\t ___/ / /___/ /___/ /_/ / _, _/ /___   / /_/ / /_/ / /_/ / 
\t/____/_____/\____/\____/_/ |_/_____/  /_____/_____/_____/ 

\t_______________________________________________________________\033[0m

""")

def connect():
    """
    Crée un socket client et se connecte au serveur.
    
    Returns:
        client (socket.socket): Le socket client créé.
    """
    
    # Créer un socket client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Se connecter au serveur
    client.connect((socket.gethostname(), PORT))
    return client

def wait_key(end:bool=True):
    """
    Attend l'appui d'une touche sur le clavier pour continuer.
    
    Args:
        end (bool, optional): Détermine si le message d'attente est affiché à la fin. 
                             Par défaut True pour afficher le message.
    """
    if end:
        input("\n\033[93mAppuyer sur une touche pour continuer ...\033[0m")
    print("\033c", end="")
    header()

def start():
    try:
        #Par souci de simplicité, nous allons faire une requète directement sur la bdd directement coté client afin de créer la database
        from serveur.connect_bdd import create_database
        create_database(DATABASE, VERBOSE)
    except:
        pass

    from serveur.connect_bdd import create_table
    create_table(TABLE_Q31, [("items","text"), ("nombre_ope","VARCHAR(2000)"),("nombre_phe","VARCHAR(2000)"),("exposant_phe","VARCHAR(2000)")],VERBOSE)
    try:
        #Par souci de simplicité, nous allons faire une requète directement sur la bdd directement coté client afin de créer les tables dans la base de données
        from serveur.connect_bdd import create_table
        create_table(TABLE_Q31, [("items","text"), ("nombre_ope","VARCHAR(2000)"),("nombre_phe","VARCHAR(2000)"),("exposant_phe","VARCHAR(2000)")],VERBOSE)
    except Exception as e:
        input(e)
        pass

    while True:
        wait_key(False)
        print("\t\033[4mPlease select an option:\033[0m\n")
        print("\t1. Afficher le nom des tables")
        print("\t2. Afficher tous les éléments")
        print("\t3. Ajouter un/des élément(s)")
        print("\t4. Comparer 2 éléments")
        print("\t5. Somme de 2 éléments")
        print("\t6. Attaque")
        print("\n\tEnter your choice (1-6)")
        print("\t\033[90mExit : q\033[0m\n")
        choice = input("\t\033[5m>> \033[0m")
        wait_key(False)

        if choice == "1":
            message = (1,[TABLE_Q31, VERBOSE])

            message = pickle.dumps(message)
            client = connect(); client.send(message)
            reponse = client.recv(1024); reponse = pickle.loads(reponse)
            client.close()

            column_number = 0
            for column in reponse:
                print(f"\033[96mColonne {column_number}\033[0m: {column[0]}")
                print("-------------------------")
                column_number += 1
            wait_key()
        
        elif choice == "2":
            from client.chiffrement import decrypt_value, KEY
            message = (2,[TABLE_Q31, VERBOSE])
            message = pickle.dumps(message)
            client = connect(); client.send(message)
            BUFFER_SIZE = 4096

            # Recevoir des données du client
            response = bytearray()
            while True:
                data = client.recv(BUFFER_SIZE)
                if not data:
                    break
                response += data

            # Traiter la réponse
            reponse = pickle.loads(response)
            client.close()
            for item in reponse:
                print(f"\033[92mItem\033[0m: {item[0]}")
                decrypted_value = decrypt_value(int(item[1]), KEY, VERBOSE)
                print(f"\033[92mPrice\033[0m: {decrypted_value} €")
                print("-----------")
            wait_key()

        elif choice == "3":
            from client.chiffrement import chiffrement_value_ope, chiffrement_value_phe, KEY, public_key
            add_element = input("\033[94mElement à ajouter:\033[0m  ")
            prix_element = input("\033[94mPrix (€) :\033[0m  ")

            encrypted_number_ope = chiffrement_value_ope(int(prix_element), KEY, VERBOSE)
            encrypted_number_phe = chiffrement_value_phe(int(prix_element), public_key, VERBOSE)

            message = (3,[TABLE_Q31, add_element, encrypted_number_ope,encrypted_number_phe[0], encrypted_number_phe[1],VERBOSE])
            message = pickle.dumps(message)
            client = connect()
            client.send(message)
            BUFFER_SIZE = 4096

            # Recevoir des données du client
            response = bytearray()
            while True:
                data = client.recv(BUFFER_SIZE)
                if not data:
                    break
                response += data

            # Traiter la réponse
            reponse = pickle.loads(response)
            client.close()
            print("\n\033[92mNombre ajouté\033[0m")
            wait_key()
        
        elif choice == "4":
            first_item = input("\033[94mPremier élément:\033[0m  ") 
            second_item = input("\033[94mSecond élément:\033[0m  ") 
            message = (4,[TABLE_Q31, first_item, second_item, "ope", VERBOSE])
            message = pickle.dumps(message)
            client = connect()
            client.send(message)
            BUFFER_SIZE = 4096

            # Recevoir des données du client
            response = bytearray()
            while True:
                data = client.recv(BUFFER_SIZE)
                if not data:
                    break
                response += data

            # Traiter la réponse
            reponse = pickle.loads(response)
            client.close()
            json_input = {first_item:reponse[0][0][0], second_item:reponse[1][0][0]}
            input(json_input)
            from client.chiffrement import order_guarantees_ope
            diff_values = order_guarantees_ope(json_input, VERBOSE)
            diff_values.reverse()
            ii = 0
            while ii < len(diff_values):
                print(f"{diff_values[ii][0]} \033[91m >\033[0m {diff_values[ii+1][0]}")
                ii += 2
            wait_key()
        
        elif choice == "5":
            first_item = input("\033[94mPremier élément: \033[0m") 
            second_item = input("\033[94mSecond élément: \033[0m") 
            message = (4,[TABLE_Q31, first_item, second_item, "phe", VERBOSE])
            message = pickle.dumps(message)
            client = connect()
            client.send(message)
            BUFFER_SIZE = 4096

            # Recevoir des données du client
            response = bytearray()
            while True:
                data = client.recv(BUFFER_SIZE)
                if not data:
                    break
                response += data

            # Traiter la réponse
            reponse = pickle.loads(response)
            client.close()
            from client.chiffrement import somme_value_phe, public_key, dechiffrement_value_phe, private_key
            diff_values = somme_value_phe([reponse[0][0], reponse[1][0]], public_key)
            print(diff_values)
            somme_decrypted = dechiffrement_value_phe(diff_values.ciphertext(), private_key)

            print(f"\033[96mLa somme des 2 produits est de \033[0m: {somme_decrypted}")
            wait_key()
        
        elif choice == "6":
            name = input("\033[94mElément: \033[0m") 
            message = (5,[TABLE_Q31, "*", VERBOSE])
            message = pickle.dumps(message)
            client = connect()
            client.send(message)
            BUFFER_SIZE = 4096

            # Recevoir des données du client
            response = bytearray()
            while True:
                data = client.recv(BUFFER_SIZE)
                if not data:
                    break
                response += data

            # Traiter la réponse
            reponse = pickle.loads(response)
            client.close()

            json_input = {}
            aug = 0
            for ii in reponse:
                json_input["a"+str(aug)] = int(ii[0])
                aug+=1
            from client.chiffrement import order_guarantees_ope
            diff_values = order_guarantees_ope(json_input, VERBOSE)

            diff_values = [int(x) for _, x in diff_values]
            diff_values.reverse()
            message = (5,[TABLE_Q31, name, VERBOSE])
            message = pickle.dumps(message)
            client = connect()
            client.send(message)
            BUFFER_SIZE = 4096

            # Recevoir des données du client
            response = bytearray()
            while True:
                data = client.recv(BUFFER_SIZE)
                if not data:
                    break
                response += data

            # Traiter la réponse
            reponse = pickle.loads(response)[0][0]
            print(reponse)
            client.close()
            index = diff_values.index(int(reponse))
            print(f"Position : {index}")
            tt = len(diff_values)
            if index <= 0.1*tt:
                print(f"Salaire inférieur à 1000 euros")
            elif index > 0.1*tt and index <= 0.3*tt:
                print(f"Salaire entre 1000 et 2500 euros")
            elif index > 0.3*tt and index <= 0.55*tt:
                print(f"Salaire entre 2500 et 4000 euros")
            elif index > 0.55*tt and index <= 0.65*tt:
                print(f"Salaire entre 4000 et 6000 euros")
            elif index > 0.65*tt and index <= 0.85*tt:
                print(f"Salaire entre 6000 et 10000 euros")
            elif index > 0.85*tt and index <= tt:
                print(f"Salaire entre 10000 et 20000 euros")

            print("Verification:\n")
            from client.chiffrement import decrypt_value, KEY
            decrypted_value = decrypt_value(int(reponse), KEY, VERBOSE)
            print(f"\033[92mPrice\033[0m: {decrypted_value} €")
            wait_key()
        
        elif str(choice).lower() == "q":
            print("\033[91mExiting...\033[0m")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__  == "__main__":
    start()
