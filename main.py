import datetime
import requests
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date

def start():
    choix = int(input("Que souhaitez-vous ?\n\n1) Vérifier les attaques de ce jour\n2) Vérifier les attaques d'une date antérieure\n\nChoix : "))

    while choix not in [1,2]:
        print("\n##################\nERREUR DE SAISIE\n")
        choix = int(input("Que souhaitez-vous ?\n\n1) Vérifier les attaques de ce jour\n2) Vérifier les attaques d'une date antérieure\n\nChoix : "))

    return choix

# Recupérer la date du jour au format aaaa-mm-jj
def date_aaaa_mm_jj():
    today = date.today()

    return today

def date_amj_to_jma():
    now = datetime.datetime.now()
    date_format_mail = now.strftime("%d-%m-%Y")

    return date_format_mail

def date_user():
    date = input("Renseigner une date au format aaaa-mm-jj\nSaisie : ")

    return date

# Scrapping du tableau du site ransomware.live
def scrapping_raas():
    lien_raas = "https://privtools.github.io/ransomposts/"
    requete = requests.get(lien_raas).text
    dataframe = pd.read_html(requete)
    liste_donnees = dataframe[0].values.tolist()

    return liste_donnees

# Trier la liste en ne gardant que les revendications du jour
def tri_tableau(liste_donnees, choix):
    liste_raas = []

    if choix == 1:
        date = date_aaaa_mm_jj()

        for donnee in liste_donnees:

            if str(date) == donnee[2][:10]:
                donnee[2] = donnee[2][:10]
                liste_raas.append(donnee)

        nb_raas = len(liste_raas)

    else:
        date = date_user()

        for donnee in liste_donnees:

            if date == donnee[2][:10]:
                donnee[2] = donnee[2][:10]
                liste_raas.append(donnee)

        nb_raas = len(liste_raas)

    return liste_raas, nb_raas, date


# Affichage de la liste des attaques du jour revendiquées
def affichage_liste(liste_raas, nb_raas, date):
    i = 0

    if nb_raas == 0:
        print(f"Aucune attaque n'a été revendiquée le {date}")

    else:
        print(f"Le {date}, il y a eu {nb_raas} revendications d'attaques par ransomware : \n")

        while i < nb_raas:
            print(f"{i+1}) Attaquant : {liste_raas[i][1]} | Organisme attaqué : {liste_raas[i][0]}")
            i+=1

def choix_mail():
    choix_envoi_mail = int(input("Souhaitez-vous envoyer un mail d'alerte ?\n\n1) Oui\n2) Non\n\nChoix : "))
    
    while choix_envoi_mail not in [1, 2]:
        print("\n##################\nERREUR DE SAISIE\n")
        choix_envoi_mail = int(input("Souhaitez-vous envoyer un mail d'alerte ?\n\n1) Oui\n2) Non\n\nChoix : "))
    
    return choix_envoi_mail

# Envoyer un mail de synthèse
def envoi_mail(nb_raas, liste_raas, date):
    i = 0

    message = MIMEMultipart()
    message["To"] = 'INSERER MAIL RECEPTEUR'
    message["From"] = 'Alerte Ransomware'
    message["Subject"] = f'Bilan Ransomware - {date}'

    if nb_raas == 0:
        messageText = (f"Aucune attaque n'a été revendiquée le {date}.")

    else:
        msg = (f"Bilan des {nb_raas} attaques par ransomware du {date} :<br>")

        while i < nb_raas:
            msg += f'''<br>{i+1}) Attaquant : {liste_raas[i][1]} | Organisme attaqué : {liste_raas[i][0]}'''
            i+=1

        messageText = MIMEText(msg, 'html')

    message.attach(messageText)

    email = 'INSERER MAIL ENVOI'
    password = 'MDP APPLICATION'

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo('Gmail')
    server.starttls()
    server.login(email, password)
    fromaddr = email
    toaddrs = message["To"]
    server.sendmail(fromaddr, toaddrs, message.as_string())

    server.quit()

if __name__ == '__main__':
    choix = start()
    liste_donnees = scrapping_raas()
    liste_raas, nb_raas, date = tri_tableau(liste_donnees, choix)
    affichage_liste(liste_raas, nb_raas, date)
    choix_envoi_mail = choix_mail()
    if choix_envoi_mail == 1:
        envoi_mail(nb_raas, liste_raas, date)

#Ajout dans CaillouNoir
