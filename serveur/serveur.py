# Côté serveur
import socket
import pickle
import sys, os
import json
sys.path.append('libs')
sys.path.append(os.getcwd())

PATH_CONFIG = "Config/config.json"
configuration = json.loads(open(PATH_CONFIG,"r").read())

PORT  = configuration["PORT_SOCKET"]

# Créer un socket serveur
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = (socket.getfqdn()) # or socket.getfqdn() if the former doesn't work
print(host)
serveur.bind((host, PORT))

# Écouter les connexions entrantes
serveur.listen(1)
print("Server START")

def start():
    """
        Fonction principale pour gérer les connexions clients et les messages reçus.
    """
    while True:

        # Accepter une connexion
        client, adresse = serveur.accept()
        print(f"Connexion établie avec {adresse}")

        # Recevoir un message du client
        message = client.recv(1024)
        message = pickle.loads(message)
        print(f"Message reçu: {message}")
    
        if message[0] == 1:
            TABLE_Q31 = message[1][0]
            VERBOSE = message[1][1]
            from connect_bdd import list_table
            list_column_table = list_table(TABLE_Q31,VERBOSE)
            
            # Envoyer une réponse au client
            reponse = list_column_table
            print(reponse)
            reponse = pickle.dumps(reponse)

            client.send(reponse)

            # Fermer la connexion
            client.close()
        elif message[0] == 2:
            TABLE_Q31 = message[1][0]
            VERBOSE = message[1][1]
            from connect_bdd import list_item_in_bdd
            list_item = list_item_in_bdd(TABLE_Q31,VERBOSE)
            # Envoyer une réponse au client
            reponse = list_item
            print(reponse)
            reponse = pickle.dumps(reponse)
            client.send(reponse)
            client.close()

        elif message[0] == 3:
            from connect_bdd import add_item_in_bdd
            TABLE_Q31 = message[1][0]
            add_element = message[1][1]
            encrypted_number_ope =message[1][2]
            encrypted_number_phe_1 = message[1][3]
            encrypted_number_phe_2 = message[1][4]
            VERBOSE = message[1][4]
            response = add_item_in_bdd(TABLE_Q31,[("items",add_element),("nombre_ope",str(encrypted_number_ope)),("nombre_phe",str(encrypted_number_phe_1)),("exposant_phe",str(encrypted_number_phe_2))], VERBOSE)
            print(response)
            reponse = pickle.dumps("True")

            client.send(reponse)
            client.close()
        
        elif message[0] == 4:
            from connect_bdd import get_value
            TABLE_Q31 = message[1][0]
            first_item = message[1][1]
            second_item =message[1][2]
            opp = message[1][3]
            VERBOSE = message[1][4]

            value1 = get_value(TABLE_Q31, [first_item], opp, VERBOSE)
            value2 = get_value(TABLE_Q31, [second_item], opp, VERBOSE)
            response = (value1,value2)
            print(response)
            reponse = pickle.dumps((value1,value2))

            client.send(reponse)
            client.close()

        elif message[0] == 5:
            from connect_bdd import get_value
            TABLE_Q31 = message[1][0]
            first_item = message[1][1]
            VERBOSE = message[1][2]

            value1 = get_value(TABLE_Q31, [first_item], "ope", VERBOSE)
            response = (value1)
            print(response)
            reponse = pickle.dumps((value1))

            client.send(reponse)
            client.close()

if __name__ == "__main__":
    start()