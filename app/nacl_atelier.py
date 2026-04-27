import os
import sys
import binascii
import nacl.secret
import nacl.utils
from nacl.exceptions import CryptoError

def get_key():
    # On récupère la clé depuis l'environnement (format hexadécimal)
    key_hex = os.getenv("NACL_KEY")
    
    if not key_hex:
        print("❌ ERREUR : La variable d'environnement NACL_KEY est introuvable.")
        print("Pour générer une clé valide, exécutez cette commande dans le terminal :")
        print('python -c "import nacl.utils, binascii; print(binascii.hexlify(nacl.utils.random(32)).decode())"')
        sys.exit(1)
        
    try:
        # On reconvertit la chaîne hexadécimale en octets bruts (32 bytes)
        return binascii.unhexlify(key_hex)
    except Exception:
        print("❌ ERREUR : Le format de la clé NACL_KEY est invalide. Elle doit être en hexadécimal.")
        sys.exit(1)

def process_file(action, input_path, output_path):
    key = get_key()
    
    # Initialisation de la SecretBox avec notre clé de 32 octets
    box = nacl.secret.SecretBox(key)

    try:
        # Lecture du fichier source
        with open(input_path, 'rb') as file:
            original_data = file.read()

        if action == 'encrypt':
            # SecretBox génère un nonce aléatoire et le préfixe automatiquement au résultat
            processed_data = box.encrypt(original_data)
            print(f"🔒 Fichier chiffré avec succès : {output_path}")
            
        elif action == 'decrypt':
            # SecretBox extrait automatiquement le nonce et vérifie l'intégrité (Poly1305)
            processed_data = box.decrypt(original_data)
            print(f"🔓 Fichier déchiffré avec succès : {output_path}")
            
        else:
            print("❌ Action non reconnue. Utilisez 'encrypt' ou 'decrypt'.")
            sys.exit(1)

        # Écriture du fichier de sortie
        with open(output_path, 'wb') as file:
            file.write(processed_data)

    except FileNotFoundError:
        print(f"❌ ERREUR : Le fichier source '{input_path}' est introuvable.")
        sys.exit(1)
    except CryptoError:
        # Cette erreur se déclenche si la clé est mauvaise, ou si le fichier a été altéré
        print("❌ ERREUR CRITIQUE : Échec du déchiffrement. Clé incorrecte ou données corrompues !")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERREUR inattendue : {e}")
        sys.exit(1)

# --- Point d'entrée du script ---
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Utilisation : python app/nacl_atelier.py <encrypt|decrypt> <fichier_entree> <fichier_sortie>")
        sys.exit(1)

    action_demandee = sys.argv[1]
    fichier_in = sys.argv[2]
    fichier_out = sys.argv[3]

    process_file(action_demandee, fichier_in, fichier_out)