import os, platform, sys, argparse, subprocess

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

# Fonction pour calculer le masque
def calcul_mask(premier, deuxieme, troisieme, quatrieme):
    masque_bin = int(premier) * 256**3 + int(deuxieme) * 256**2 + int(troisieme) * 256 + int(quatrieme)
    masque_long = bin(masque_bin).count("1")
    return masque_long

# Fonction menu et choix de l'interface
def menu_interface(network):
    # Proposer un menu pour choisir l'interface réseau
    print("Voici les interfaces détectées sur votre poste : ")

    # Afficher les réseaux
    for i, iface in enumerate(network):
        print(f"Réseau {i} - {iface}")

    # Sélection d'une interface
    choix = int(input("Choisissez l'interface à scanner : "))

    if choix < 0 or choix >= len(network):
        print("Choix invalide.")
        return

    # Afficher le réseau sélectionné
    print("Vous avez choisi le réseau : " + network[choix])

    # Scanner le réseau avec nmap
    try:
        nmap = subprocess.run(["nmap", "-sn", network[choix]], capture_output=True, text=True)
        print(nmap.stdout)
        # Mettre la sortie de la commande dans le fichier
        ecrire_fichier("nmap.txt", nmap.stdout)
    except FileNotFoundError:
        print("L'outil nmap n'est pas installé. Veuillez l'installer pour utiliser cette fonctionnalité.")

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE PRINCIPAL 
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Créer une aide pour "-h"
parser = argparse.ArgumentParser(description="Pour récupérer le type d'OS ainsi que les adresses IP, exécutez le programme python.")
args = parser.parse_args()

network = []

if "Linux" in platform.uname():
    # Je suis sous Linux
    try:
        print("Système d'exploitation : Linux")
    except Exception as e:
        print(f"Error: {e}")    # Ce qu'il faut faire
        # print("Error" + e)    # Ce qu'il ne faut pas faire

    # Récupérer la configuration IP
    ifconfig = subprocess.run(["/usr/sbin/ip", "a"], capture_output=True, text=True)

    # Ecrire la confiration IP dans un fichier
    ecrire_fichier("ipa.txt", ifconfig.stdout)

    # Récupérer et lister le répertoire du fichier
    print(lister_fichier())

    # Lire le fichier créée
    contenu = lire_fichier("ipa.txt")
    print(contenu)
        
    # Récupérer les adresses IP
    print('Voici les IPv4 récupérées dans le fichier :')
    for ligne in contenu.splitlines():
        if "inet " in ligne:
            # Trouver la ligne qui commence par "inet "
            addr_start = ligne.find("inet ")
            if addr_start != -1:
                # Extraire l'adresse IP en utilisant une découpe
                addr = ligne[addr_start + 5:].split()[0]
                network.append(addr)

    # Afficher les IP
    print(network)

    # Afficher le menu pour choisir l'interface réseau
    menu_interface(network)


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

    # Récupérer les adresses IP et les masques
    print('Voici les IPv4 récupérées dans le fichier :')
    for ligne in contenu.splitlines():
        if "Adresse IPv4" in ligne:
            network_ip = ligne.split(": ")[1]

        if "Masque" in ligne:
                # Stocker le masque
                masque = ligne.split(":")[1]
                premier = masque.split(".")[0]
                deuxième = masque.split(".")[1]
                troisième = masque.split(".")[2]
                quatrième = masque.split(".")[3]

                # Caluler le masque
                masque_calc = calcul_mask(premier, deuxième, troisième, quatrième)

                # Concatenation de l'ip et du masque dans un tableau
                network.append(network_ip + "/" + str(masque_calc))
    
    # Afficher le menu pour choisir l'interface réseau
    menu_interface(network)

else:
    # Je ne sais pas où je suis
    print("Unknown ???")
