import threading, scapy.all as scapy
from queue import Queue
from scapy.layers.inet import IP
from scapy.all import rdpcap

# Fonction d'affichage direct
def print_info(sniff):
    print(sniff.summary())

def tri_packet(packets, resultats):
    ip_couples = []

    # Parcourir tous les paquets et extraires les IP S/D
    for packet in packets:
        if IP in packet:
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            ip_couple = (ip_src, ip_dst)
            ip_couples.append(ip_couple)

    resultats.put(ip_couples)

if __name__ == '__main__':
    # Proposer l'interface à l'utilisateur
    print("Voici les interfaces disponibles :")
    interfaces = scapy.get_if_list()
    print(interfaces)
    choix = int(input("Choisissez l'interface à scanner : "))
    
    # Sniffer tout le réseau sans limite de paquet et de manière directe
    sniff = scapy.sniff(iface=interfaces[choix], prn=print_info)
    
    try:
        # Enregistrer les paquets capturés dans un fichier pcap
        pcap_filename = "/home/jiullian/Documents/captured_packets.pcap"
        scapy.wrpcap(pcap_filename, sniff)
        print(f"Les paquets ont été enregistrés dans {pcap_filename}")

        # Initialiser un tableau pour stocker les couples
        packets = rdpcap(pcap_filename)
    except:
        print("Erreur lors de l'enregistrement des paquets")

    # Divier la liste en 2 parties
    moitie = int(len(packets)/2)
    packets1 = packets[:moitie]
    packets2 = packets[moitie:]

    # Définition d'une queue pour stocker les résultats du thread
    resultats = Queue()

    try:
        # Création des threads
        th1 = threading.Thread(target=tri_packet, args=(packets1, resultats))
        th2 = threading.Thread(target=tri_packet, args=(packets2, resultats))
    except:
        print("Erreur lors de la création du thread")

    # Lancement des threads
    th1.start()
    th2.start()

    # Attendre la fin des threads
    th1.join()
    th2.join()

    # Récupérer les résultats des threads
    ip_couples1 = resultats.get()
    ip_couples2 = resultats.get()

    # Fusionner les résultats
    ip_couples = ip_couples1 + ip_couples2

    # Eviter les doublons en utilisant un set
    unique = set(ip_couples)

    if not unique :
        # Affichage des couples uniques
        print("Aucun couple unique n'a été trouvé")
    else :
        print("Voici les couples uniques :")
        print("Source   |   Destination")
        for ip_couple in unique :
            print(ip_couple)
