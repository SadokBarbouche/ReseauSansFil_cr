import subprocess
import re
import platform
from datetime import datetime
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation

Signal, Time = [], []

figure = pyplot.figure()  # Initialisation de la figure
line, = pyplot.plot_date(Signal, Time)  # Initialisation de la ligne de courbe


def read_data_from_cmd():
    cmd = "netsh wlan show interfaces"  # Commande a executer
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    if p.returncode == 0:
        out = p.stdout.read().decode('unicode_escape').strip()
        if platform.system() == 'Windows':
            m = re.findall('SSID.*?ÿ:.*?([A-z0-9 ]*).*?Signal.*?ÿ:.*?([0-9]*)%', out, re.DOTALL)
        else:
            raise Exception('OS non reconnu !')
        p.communicate()
        return m


title = read_data_from_cmd()[0][0]


def animate(frame):
    Time.append(datetime.now())
    Signal.append(int(read_data_from_cmd()[0][1]))
    line.set_data(Time, Signal)
    figure.gca().relim()
    figure.gca().autoscale_view()
    return line,


animation = FuncAnimation(figure, animate, interval=500)
pyplot.title("Connected to: "+title)
pyplot.xlabel("Time")
pyplot.ylabel("Signal Strength")
pyplot.show()
