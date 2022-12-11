"""
    Pour compiler ce code , veuillez changer l'emplacement du fichier Wireshark à analyser
    Travail de :
        Barbouche Sadok
        Mtiri Wissem
    Groupe :
        RT 3-2
"""


import argparse
import os
from time import sleep
import sys
from scapy.utils import PcapReader
from scapy.layers.dot11 import *
#from scapy.packet import Packet
from scapy.all import *


def process_pcap():
    print('Opening {}...'.format(FILE_NAME))
    for dot11_packet in PcapReader(FILE_NAME):
#    for (pkt_data, pkt_metadata,) in RawPcapReader(FILE_NAME):
#       dot11_packet = Dot11(pkt_data)
        print(dot11_packet.summary())
        
                

def parse(frame):
    if frame.haslayer(Dot11):
        print("ToDS:", frame.FCfield & 0b1 != 0)
        print("MF:", frame.FCfield & 0b10 != 0)
        print("WEP:", frame.FCfield & 0b01000000 != 0)
        print("src MAC:", frame.addr2)
        print("dest MAC:", frame.addr1)
        print("BSSID:", frame.addr3)
        print("Duration ID:", frame.ID)
        print("Sequence Control:", frame.SC)
        print("\n")
    
    

def attempts_number():
    # Ouvrir le fichier PCAP
    pcap = rdpcap("D:\wireshark.pcapng")
    # Initialiser le compteur des tentatives d'association
    association_count = 0
    # Pour chaque paquet dans le fichier PCAP
    for packet in pcap:
        # Si le paquet est une trame d'association
        if packet.haslayer(Dot11AssoReq):
            # Incrémenter le compteur des tentatives d'association
            association_count += 1
    # Afficher le nombre de tentatives d'association
    print("Nombre de tentatives d'association:", association_count)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='PCAP reader')
    parser.add_argument('--pcap', metavar='<pcap file name>',
                        help='pcap file to parse',required=True)
    args = parser.parse_args()
    global FILE_NAME
    FILE_NAME = args.pcap
    if not os.path.isfile(FILE_NAME):
        print(' "{}" does not exist '.format(FILE_NAME), file=sys.stderr)
        sys.exit(-1)
    process_pcap()
    print("************************************************************************")
    sniff(offline="D:\wireshark.pcapng", prn=parse)     
    print("************************************************************************\n")
    attempts_number()
    sys.exit(0)
    
    
    