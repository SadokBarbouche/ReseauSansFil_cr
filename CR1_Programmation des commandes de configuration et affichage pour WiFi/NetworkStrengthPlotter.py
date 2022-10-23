import subprocess
import re
import platform
from datetime import datetime
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation

def wifiStrengthPlotter():
    # ASCII ART
    print('''
    
    ░██╗░░░░░░░██╗██╗███████╗██╗  ░██████╗████████╗██████╗░███████╗███╗░░██╗░██████╗░████████╗██╗░░██╗
    ░██║░░██╗░░██║██║██╔════╝██║  ██╔════╝╚══██╔══╝██╔══██╗██╔════╝████╗░██║██╔════╝░╚══██╔══╝██║░░██║
    ░╚██╗████╗██╔╝██║█████╗░░██║  ╚█████╗░░░░██║░░░██████╔╝█████╗░░██╔██╗██║██║░░██╗░░░░██║░░░███████║
    ░░████╔═████║░██║██╔══╝░░██║  ░╚═══██╗░░░██║░░░██╔══██╗██╔══╝░░██║╚████║██║░░╚██╗░░░██║░░░██╔══██║
    ░░╚██╔╝░╚██╔╝░██║██║░░░░░██║  ██████╔╝░░░██║░░░██║░░██║███████╗██║░╚███║╚██████╔╝░░░██║░░░██║░░██║
    ░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░░░░╚═╝  ╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚══════╝╚═╝░░╚══╝░╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝
    
    ██████╗░██╗░░░░░░█████╗░████████╗████████╗███████╗██████╗░
    ██╔══██╗██║░░░░░██╔══██╗╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗
    ██████╔╝██║░░░░░██║░░██║░░░██║░░░░░░██║░░░█████╗░░██████╔╝
    ██╔═══╝░██║░░░░░██║░░██║░░░██║░░░░░░██║░░░██╔══╝░░██╔══██╗
    ██║░░░░░███████╗╚█████╔╝░░░██║░░░░░░██║░░░███████╗██║░░██║
    ╚═╝░░░░░╚══════╝░╚════╝░░░░╚═╝░░░░░░╚═╝░░░╚══════╝╚═╝░░╚═╝
    
    ''')
    # Declare empty lists
    Signal, Time = [], []

    figure = pyplot.figure()  # Initialisation de la figure
    line, = pyplot.plot_date(Signal, Time, '-')  # Initialisation de la ligne de courbe

    def read_data_from_cmd():
        cmd = "netsh wlan show interfaces"  # Commande a executer
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) #Start a subprocess
        p.wait() # Wait till the subprocess finishes executing
        if p.returncode == 0: # Subprocess finished successfully
            out = p.stdout.read().decode('unicode_escape').strip() # decode the result
            if platform.system() == 'Windows': # Only windows OS case is treated
                m = re.findall('SSID.*?ÿ:.*?([A-z0-9 ]*).*?Signal.*?ÿ:.*?([0-9]*)%', out, re.DOTALL) # Searching for desired fields using Regex
            else:
                raise Exception('OS non reconnu !')
            p.communicate()
            print("Strength = " + m[0][1])
            return m
    title = read_data_from_cmd()[0][0] # Set title
    print("Connected to "+ title)

    def animate(frame):
        Time.append(datetime.now()) # Adds time data to the Time list initially declared
        Signal.append(int(read_data_from_cmd()[0][1])) # Adds signal data to the Signal list initially declared
        line.set_data(Time, Signal)
        figure.gca().relim() # changing axes limits
        figure.gca().autoscale_view() # Changing scales according to current values
        return line,


    animation = FuncAnimation(figure, animate, interval=500)
    pyplot.title("Connected to: "+title)
    pyplot.xlabel("Time")
    pyplot.ylabel("Signal Strength")
    pyplot.show()


