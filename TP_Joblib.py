import scapy.all as scapy
from scapy.layers.inet import IP
from scapy.all import rdpcap
from joblib import Parallel, delayed
from queue import Queue

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
    packetstableau = [packets[:moitie], packets[moitie:]]

    # Définition d'une queue pour stocker les résultats des processus
    resultats = Queue()

    
    try:
        # Création d'un processus
        function = delayed(tri_packet)
        p = Parallel(n_jobs=1)(function(packetstableau[i],resultats) for i in range(len(packetstableau)))
    except:
        print("Erreur lors de la création du processus")

    # Rassembler les résultats de tous les processus
    ip_couples = []
    while not resultats.empty():
        ip_couples.extend(resultats.get())

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
