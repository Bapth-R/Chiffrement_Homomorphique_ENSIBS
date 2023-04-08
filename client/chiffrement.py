import sys, os
sys.path.append('libs')

from dotenv import load_dotenv
from pyope.ope import OPE, ValueRange
from phe import paillier

sys.path.append(os.getcwd())
load_dotenv("Config/.env")

PUBLIC_KEY_PHE = os.environ["PUBLIC_KEY_PHE"]
PRIVATE_KEY_PHE1 = os.environ["PRIVATE_KEY_PHE_1"]
PRIVATE_KEY_PHE2 = os.environ["PRIVATE_KEY_PHE_2"]

KEY = bytes(os.environ["KEY"], encoding='utf8')

public_key= paillier.PaillierPublicKey(int(PUBLIC_KEY_PHE))
private_key = paillier.PaillierPrivateKey(public_key, int(PRIVATE_KEY_PHE1), int(PRIVATE_KEY_PHE2))

##### Chiffrement OPE #####

def chiffrement_value_ope(value:int, key:bytes, verbose:bool=False):
    """
        Chiffre une valeur à l'aide de l'algorithme OPE.
    Args:
        value (int): La valeur à chiffrer.
        key (bytes): La clé de chiffrement.
        verbose (bool): Affiche des informations supplémentaires si True. Par défaut False.
    Returns:
        (cipher.encrypt()): La valeur chiffrée ou False si une erreur se produit.
    """

    try:
        cipher = OPE(key,in_range=ValueRange(0, 1000000),
                              out_range=ValueRange(0, 1000000000000))
    except Exception as e:
        return False
    return (cipher.encrypt(value))

def order_guarantees_ope(value_encrypted:dict, verbose:bool=False):
    """
        Teste si l'encryption est préservée à l'ordre.

    Args:
        value_encrypted (dict): Dictionnaire contenant les valeurs chiffrées.
        verbose (bool): Affiche des informations supplémentaires si True. Par défaut False.
    Return:
        sorted_data: Les valeurs triées par ordre croissant ou False si une erreur se produit.
    """
    try:

        sorted_data = sorted(value_encrypted.items(), key=lambda x: x[1],reverse=True)
    except Exception as e:
        print(e)
        return False
    return sorted_data 

def decrypt_value(encrypt_value:int, key:str, verbose:bool=False):
    """
        Déchiffre une valeur chiffrée à l'aide de l'algorithme OPE.

    Args:
        encrypt_value (int): La valeur chiffrée.
        key (str): La clé de chiffrement.
        verbose (bool): Affiche des informations supplémentaires si True. Par défaut False.
    Returns:
        cipher.decrypt(): La valeur déchiffrée ou False si une erreur se produit.
    """
    DEFAULT_IN_RANGE_START = 0
    DEFAULT_IN_RANGE_END = 2**15 - 1


    try:
                cipher = OPE(key,in_range=ValueRange(0, 1000000),
                              out_range=ValueRange(0, 1000000000000))
    except Exception as e:
        print(e)
        print("ERROR")
        return False
    return cipher.decrypt(encrypt_value)


##### Chiffrement PHE #####
def chiffrement_value_phe(value:int, pubkey, verbose:bool=False):
    """
    Chiffre la valeur fournie en utilisant la clé publique fournie et renvoie les valeurs chiffrées.

    Args:
        value (int): Valeur à chiffrer.
        pubkey: Clé publique utilisée pour chiffrer.
        verbose (bool, optional): Si vrai, affiche des messages de débogage. Defaults to False.

    Returns:
        tuple: Les valeurs chiffrées : le texte chiffré et l'exposant.

    """
    try:
        value_encrypted = pubkey.encrypt(value)
    except:
        return False 
    return value_encrypted.ciphertext(), value_encrypted.exponent
            
def somme_value_phe(items:list, public_key:int, verbose:bool=False):
    """
        Calcule la somme des valeurs chiffrées fournies en utilisant la clé publique fournie.
    Args:
        items (list): Liste d'éléments chiffrés sous forme de dictionnaires contenant les clés 'ciphertext' et 'exponent'. Ex : [{"ciphertext":23141324,"exponent":0},{"ciphertext":2314314,"exponent":0},{"ciphertext":14141324,"exponent":0}]
        public_key: Clé publique utilisée pour déchiffrer.
        verbose (bool, optional): Si vrai, affiche des messages de débogage. Defaults to False.

    Returns:
        paillier.EncryptedNumber: La somme des valeurs chiffrées.
    """
    somme = 0
    for item in items:
        try:
            somme += paillier.EncryptedNumber(public_key, int(item[0]), int(item[1]))
        except:
            return False
            
    return somme

def dechiffrement_value_phe(value, private_key, verbose:bool=False):
    """
    Déchiffre la valeur fournie en utilisant la clé privée fournie.

    Args:
        value: Valeur chiffrée.
        private_key: Clé privée utilisée pour déchiffrer.
        verbose (bool, optional): Si vrai, affiche des messages de débogage. Defaults to False.

    Returns:
        int: La valeur déchiffrée.

    """
    
    try:
        value = paillier.EncryptedNumber(public_key, (value), 0)
    except:
        return False

    return private_key.decrypt(value)




if __name__ == "__main__":
    value1 = 4000
    value2 = 10



    number_encrypted_ope1 = chiffrement_value_ope(value1,KEY)
    number_encrypted_ope2 = chiffrement_value_ope(value2,KEY)

    print("TEST ORDER OPE")
    #print(test_order_guarantees_ope([number_encrypted_ope1, number_encrypted_ope2], [4000,10], KEY))


    print("TEST ADDITION PHE")
    number_encrypted_phe1 = chiffrement_value_phe(value1,public_key)
    number_encrypted_phe2 = chiffrement_value_phe(value2,public_key)
    somme_encrypted = somme_value_phe([number_encrypted_phe1, number_encrypted_phe2], public_key)

    print(type(somme_encrypted))
    print(dechiffrement_value_phe(somme_encrypted, private_key))



