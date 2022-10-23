from tkinter import *
import subprocess
import re
import platform

def networkPlotter():
#   ASCII ART
    print('''
    
    ███╗░░██╗███████╗████████╗░██╗░░░░░░░██╗░█████╗░██████╗░██╗░░██╗  ░██████╗░█████╗░░█████╗░███╗░░██╗███╗░░██╗███████╗██████╗░
    ████╗░██║██╔════╝╚══██╔══╝░██║░░██╗░░██║██╔══██╗██╔══██╗██║░██╔╝  ██╔════╝██╔══██╗██╔══██╗████╗░██║████╗░██║██╔════╝██╔══██╗
    ██╔██╗██║█████╗░░░░░██║░░░░╚██╗████╗██╔╝██║░░██║██████╔╝█████═╝░  ╚█████╗░██║░░╚═╝███████║██╔██╗██║██╔██╗██║█████╗░░██████╔╝
    ██║╚████║██╔══╝░░░░░██║░░░░░████╔═████║░██║░░██║██╔══██╗██╔═██╗░  ░╚═══██╗██║░░██╗██╔══██║██║╚████║██║╚████║██╔══╝░░██╔══██╗
    ██║░╚███║███████╗░░░██║░░░░░╚██╔╝░╚██╔╝░╚█████╔╝██║░░██║██║░╚██╗  ██████╔╝╚█████╔╝██║░░██║██║░╚███║██║░╚███║███████╗██║░░██║
    ╚═╝░░╚══╝╚══════╝░░░╚═╝░░░░░░╚═╝░░░╚═╝░░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝  ╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝
    
    ''')

    def network_discover():
        cmd = "netsh wlan show networks mode=bssid" # Commande a executer
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = p.stdout.read().decode('unicode_escape').strip()
        p.wait()
        if platform.system() == 'Linux':
            m = re.findall('Name.*?:.*?([A-z0-9 ]*).*?Signal.*?:.*?([0-9]*)%', out, re.DOTALL)
        elif platform.system() == 'Windows':
            strength = re.findall('Signal.*?:.*?([0-9]*)%', out, re.DOTALL)
            ssid = re.findall(r'\bSSID.*?:.*?([a-zA-Z0-9_" "-]*)\r', out, re.DOTALL) # returns only the line that starts with SSID ("BSSID" wouldn't match this regex)
        else:
            raise Exception('reached else of if statement')
        return strength, ssid

    strength, ssid = network_discover()

    maxStrength = strength.index(str(max([int(i) for i in strength])))
    # Setting the interface

    root = Tk()
    root.title("Networks Scanner")
    root.geometry("640x800")

    listLabel = Label(root, text="Available Networks", font=("Consolas", 25))
    listLabel.pack(pady=20)
    myListbox = Listbox(root, width=40, height=30)
    myListbox.pack(pady=10)

    rxList = zip(ssid, strength)

    for item in list(rxList):
        print(item)
        myListbox.insert(END, "SSID: " + str(item[0]) + ' || ' + "Strength: " + str(item[1]) + '%')
    strongestLabel = Label(root, text="The strongest available Wi-Fi", font=("Consolas", 15))
    strongestLabel.pack(pady=20)
    my_label = Label(root, text="SSID = " + ssid[maxStrength] + ", Strength = " + str(strength[maxStrength]))
    my_label.pack(pady=10)

    pConnect = subprocess.Popen("netsh wlan show profiles", stdout=subprocess.PIPE, stderr=subprocess.PIPE) # look for profiles
    pConnectOut = pConnect.stdout.read().decode('unicode_escape').strip()
    pConnect.wait()
    if platform.system() == "Windows":
        profiles = re.findall('Profil Tous les utilisateurs.*?:.*?([A-z0-9 ]*)', pConnectOut, re.DOTALL)
    if str(ssid[maxStrength]) in profiles :
        p1 = subprocess.Popen("netsh wlan connect name="+str(ssid[maxStrength]), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # connect to the network with the strongest signal if it exists in profiles
        if pConnect.returncode == 0:
            print("Successfully connected !")
    root.mainloop()
    # p2 = subprocess.Popen("netsh wlan disconnect", stdout=subprocess.PIPE, stderr=subprocess.PIPE)

