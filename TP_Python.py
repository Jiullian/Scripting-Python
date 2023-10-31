import os, platform, subprocess, sys, argparse

# Fonction écriture fichier
def ecrire_fichier(nom_fichier, contenu):
    try :
        with open(nom_fichier, "w") as fichier:
          fichier.write(contenu)
    except Exception as e:
        print(f"Erreur lors de l'écriture dans %s : {e}" %(nom_fichier))

# Fonction lecture fichier
def lire_fichier(nom_fichier):
    try :
        with open(nom_fichier, "r") as fichier:
            contenu = fichier.read()
        return contenu
    except Exception as e:
        print(f"Erreur lors de la lecture de %s : {e}" %(nom_fichier))

# Fonction pour récupérer et lister le répertoire du fichier
def lister_fichier():
    try :
        dossier_courant = os.path.dirname(os.path.abspath(__file__))
        fichiers = os.listdir(dossier_courant)
        return fichiers
    except Exception as e:
        print(f"Erreur lors de la lecture du répertoire : {e}")

# Créer une aide pour "-h"
parser = argparse.ArgumentParser(description="Pour récupérer le type d'OS ainsi que les adresses IP, exécutez le programme python.")
args = parser.parse_args()

if "Linux" in platform.uname():
    # Je suis sous Linux
    try:
        print("Système d'exploitation : Linux")
    except Exception as e:
        print(f"Error: {e}")    # Ce qu'il faut faire
        # print("Error" + e)    # Ce qu'il ne faut pas faire

    # Récupérer la configuration IP
    ifconfig = subprocess.run(["ifconfig"], capture_output=True, text=True)

    # Ecrire la confiration IP dans un fichier
    ecrire_fichier("ifconfig.txt", ifconfig.stdout)

    # Récupérer et lister le répertoire du fichier
    print(lister_fichier())

    # Lire le fichier créée
    contenu = lire_fichier("ifconfig.txt")
    print(contenu)
        
    # Récupérer les adresses IP
    print('Voici les IPv4 récupérées dans le fichier :')
    for ligne in contenu.splitlines():
        if "inet " in ligne:
            # Stocker le résultat dans un tableau pour afficher seulement l'adresse IP
            print(ligne.split()[1])
                
elif "Windows" in platform.uname():
    # Je suis sous Windows
    print("Système d'exploitation : Windows")

    # Récupérer la configuration IP
    ipconfig = subprocess.run(["ipconfig"], capture_output=True, text=True)

    # Ecrire la confiration IP dans un fichier
    ecrire_fichier("ipconfig.txt", ipconfig.stdout)

    # Récupérer et lister le répertoire du fichier
    print("Voici les fichiers dans le répertoire : ")
    print(lister_fichier())

    # Lire le fichier créée
    contenu = lire_fichier("ipconfig.txt")
    print(contenu)
        
    # Récupérer les adresses IP
    print('Voici les IPv4 récupérées dans le fichier :')
    for ligne in contenu.splitlines():
        if "IPv4" in ligne:
            print(ligne)
            
else:
    # Je ne sais pas où je suis
    print("Unknown ???")
