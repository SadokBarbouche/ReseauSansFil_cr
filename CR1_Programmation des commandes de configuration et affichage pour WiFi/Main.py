from NetworkStrengthPlotter import wifiStrengthPlotter
from NetworksScanner import networkPlotter

# MENU
def main():
    print('''
    
    ████████╗██████╗░  ██████╗░██╗░░██╗
    ╚══██╔══╝██╔══██╗  ██╔══██╗╚██╗██╔╝
    ░░░██║░░░██████╔╝  ██████╔╝░╚███╔╝░
    ░░░██║░░░██╔═══╝░  ██╔══██╗░██╔██╗░
    ░░░██║░░░██║░░░░░  ██║░░██║██╔╝╚██╗
    ░░░╚═╝░░░╚═╝░░░░░  ╚═╝░░╚═╝╚═╝░░╚═╝
    
    ''')

    print("[1]: WiFi Strength Plotter")
    print("[2]: Network Scanner")
    print("[3]: Exit")

    while True:
        choice = int(input("==> "))
        if choice == 1:
            wifiStrengthPlotter()
        elif choice == 2:
            networkPlotter()
        elif choice == 3:
            exit()
        else:
            print("Wrong input! Try again\n")
            print("[1]: WiFi Strength Plotter")
            print("[2]: Network Scanner")
            print("[3]: Exit")


main()
