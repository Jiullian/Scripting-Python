import os, platform, sys, argparse, subprocess, socket, ipaddress

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# FONCTIONS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Fonction écriture fichier
def ecrire_fichier(nom_fichier, contenu, type):
    if type == "a":
        try :
            with open(nom_fichier, "a") as fichier:
              fichier.write(contenu)
        except Exception as e:
            print(f"Erreur lors de l'écriture dans %s : {e}" %(nom_fichier))
    elif type == "w":        
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

    return network[choix]

# Fonction scan réseau avec ping
def scan_network(network, OS):
    if args.output:
        ecrire_fichier("NetworkScan.txt", "Voici la liste des IP actives sur le réseau séléctionné: \n", "w")

    # Récupérer l'ip
    ip = network.split("/")[0]

    for i in range(1, 256):
        ip = ip.split(".")[0] + "." + ip.split(".")[1] + "." + ip.split(".")[2] + "." + str(i)
        if OS == "Windows":
            ping = subprocess.run(["ping", "-n", "1", ip], capture_output=True, text=True)
        elif OS == "Linux":
            ping = subprocess.run(["ping", "-c", "1", ip], capture_output=True, text=True)
        if "Impossible" not in ping.stdout and "Unreachable" not in ping.stdout:
            if args.output:
                # Exporter le résultat dans un fichier
                ecrire_fichier("NetworkScan.txt", ip + "\n", "a")
            else :
                print(f"L'hôte {ip} est actif.")

        

# Fonction pour scanner un port sur toutes les adresses IP d'un réseau
def scan_socket(subnet, ports):
    if args.output:
        ecrire_fichier("socket.txt","Résultat du scan avec le socket : \n", "w")
    for ip in ipaddress.IPv4Network(subnet, strict=False):
        ip_str = str(ip)
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.1)
                result = sock.connect_ex((ip_str, port))
                if result == 0:
                    if args.output:
                    # Exporter le résultat dans un fichier
                        ecrire_fichier("socket.txt", f"Le port {port} est ouvert sur {ip_str}", "a")
                    else :
                        print(f"Le port {port} est ouvert sur {ip_str}")
                sock.close()
            except socket.error:
                print(f"Erreur lors du scan du port {port} sur {ip_str}")

# Fonction pour les options
def options(OS):
    # Si l'option -p est utilisée
    if args.ping:
        # Afficher le menu pour choisir l'interface réseau
        choix = menu_interface(network)
        if OS == "Windows":
            scan_network(choix, "Windows")
        elif OS == "Linux":
            scan_network(choix, "Linux")
    elif args.socket:
        # Afficher le menu pour choisir l'interface réseau
        choix = menu_interface(network)
        scan_socket(choix, ports_to_scan)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# OPTIONS
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Créer une aide pour -h
parser = argparse.ArgumentParser(description="Pour récupérer le type d'OS ainsi que les adresses IP, exécutez le programme python.")
# Créer l'option -p pour utiliser le scan avec nmamp
parser.add_argument("-p", "--ping", help="Pour scanner le réseau avec nmap, ajoutez l'option -p ou --ping", action="store_true")
# Créer l'option -s pour utiliser le scan avec socket
parser.add_argument("-s", "--socket", help="Pour scanner le réseau avec socket, ajoutez l'option -s ou --socket", action="store_true")
# Créer l'option -o pour exporter le résultats dans un fichier
parser.add_argument("-o", "--output", help="Pour exporter le résultat dans un fichier, ajoutez l'option -o ou --output", action="store_true")
args = parser.parse_args()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE PRINCIPAL 
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

network = []

# Liste des ports à scanner (volontairement limitée pour ne pas trop ralentir le scan)
ports_to_scan = [80, 443]

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
    ecrire_fichier("ipa.txt", ifconfig.stdout, "w")

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

    # Déclencher la fonction des options
    options("Linux")

elif "Windows" in platform.uname():
    # Je suis sous Windows
    print("Système d'exploitation : Windows")

    # Récupérer la configuration IP
    ipconfig = subprocess.run(["ipconfig"], capture_output=True, text=True)

    # Ecrire la confiration IP dans un fichier
    ecrire_fichier("ipconfig.txt", ipconfig.stdout, "w")

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
    
    # Afficher les IP
    print(network)
    
    # Déclencher la fonction des options
    options("Windows")

else:
    # Je ne sais pas où je suis
    print("Unknown ???")
