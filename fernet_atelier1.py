import os
import sys
from cryptography.fernet import Fernet

def get_key():
    # Le script cherche la clé dans l'environnement.
    # Dans Codespaces ou GitHub Actions, GitHub l'injectera ici automatiquement.
    key = os.getenv("FERNET_KEY")
    if not key:
        print("❌ ERREUR : La variable d'environnement FERNET_KEY est introuvable.")
        print("Vérifiez que votre Secret GitHub est bien configuré et exposé dans ce Codespace.")
        sys.exit(1)
    return key

def process_file(action, input_path, output_path):
    key = get_key()
    fernet = Fernet(key)

    try:
        # Lecture du fichier source
        with open(input_path, 'rb') as file:
            original_data = file.read()

        # Chiffrement ou Déchiffrement
        if action == 'encrypt':
            processed_data = fernet.encrypt(original_data)
            print(f"🔒 Fichier chiffré avec succès : {output_path}")
        elif action == 'decrypt':
            processed_data = fernet.decrypt(original_data)
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
    except Exception as e:
        print(f"❌ ERREUR lors de l'opération : {e}")
        sys.exit(1)

# --- Point d'entrée du script ---
if __name__ == "__main__":
    # Vérification des arguments passés dans le terminal
    if len(sys.argv) != 4:
        print("Utilisation : python app/fernet_atelier1.py <encrypt|decrypt> <fichier_entree> <fichier_sortie>")
        sys.exit(1)

    action_demandee = sys.argv[1]
    fichier_in = sys.argv[2]
    fichier_out = sys.argv[3]

    process_file(action_demandee, fichier_in, fichier_out)