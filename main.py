import requests
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

def start():
    choix = int(input("Que souhaitez-vous ?\n\n1) Vérifier les attaques de ce jour\n2) Vérifier les attaques d'une date antérieure\n\nChoix : "))

    while choix not in [1,2]:
        print("\n##################\nERREUR DE SAISIE\n")
        choix = int(input("Que souhaitez-vous ?\n\n1) Vérifier les attaques de ce jour\n2) Vérifier les attaques d'une date antérieure\n\nChoix : "))

    return choix

# Recupérer la date du jour au format aaaa-mm-jj
def date_aaaa_mm_jj():
    date_du_jour = datetime.today()

    return date_du_jour

def date_amj_to_jma(date):
    date_convert_type = datetime.strptime(date, "%Y-%m-%d")

    date_format = date_convert_type.strftime("%d-%m-%Y")

    return date_format

def date_user():
    date = input("\n##################\nQuelle date souhaitez-vous consulter (format aaaa-mm-jj) ?\n\nSaisie : ")

    return date

# Scrapping du tableau du site ransomware.live
def scrapping_raas():
    lien_raas = "https://privtools.github.io/ransomposts/"
    requete = requests.get(lien_raas).text
    dataframe = pd.read_html(requete)
    liste_donnees = dataframe[0].values.tolist()

    return liste_donnees

def nb_raas_annee_actuelle(liste_donnees):
    nb_raas_annee = 0
    annee = str(date_aaaa_mm_jj())[:4]

    for donnee in liste_donnees:
        if str(annee) == donnee[2][:4]:
            nb_raas_annee += 1

    return nb_raas_annee

# Trier la liste en ne gardant que les revendications du jour
def tri_tableau(liste_donnees, choix):
    liste_raas = []

    if choix == 1:
        date = str(date_aaaa_mm_jj())[:10]

        for donnee in liste_donnees:

            if date == donnee[2][:10]:
                donnee[2] = donnee[2][:10]
                liste_raas.append(donnee)

        nb_raas = len(liste_raas)

    else:
        date = date_user()

        for donnee in liste_donnees:

            if str(date) == donnee[2][:10]:
                donnee[2] = donnee[2][:10]
                liste_raas.append(donnee)

        nb_raas = len(liste_raas)

    return liste_raas, nb_raas, date

# Affichage de la liste des attaques du jour revendiquées
def affichage_liste(liste_raas, nb_raas, date, nb_raas_annee):
    i = 0
    date_format_affichage = date_amj_to_jma(date)

    if nb_raas == 0:
        print(f"Aucune attaque n'a été revendiquée le {date_format_affichage}")

    else:
        print(f"\n##################\nDepuis début {str(date_aaaa_mm_jj())[:4]}, il y a eu {nb_raas_annee} attaques par ransomware revendiquées\n\nLe {date_format_affichage}, il y a eu {nb_raas} revendications d'attaques par ransomware : \n")

        while i < nb_raas:
            print(f"{i+1}) Attaquant : {liste_raas[i][1]} | Organisme attaqué : {liste_raas[i][0]}")
            i+=1

def choix_mail():
    choix_envoi_mail = int(input("\n##################\nSouhaitez-vous envoyer un mail d'alerte ?\n\n1) Oui\n2) Non\n\nChoix : "))

    while choix_envoi_mail not in [1, 2]:
        print("\n##################\nERREUR DE SAISIE\n")
        choix_envoi_mail = int(input("Souhaitez-vous envoyer un mail d'alerte ?\n\n1) Oui\n2) Non\n\nChoix : "))

    return choix_envoi_mail

# Envoyer un mail de synthèse
def envoi_mail(nb_raas, liste_raas, date, nb_raas_annee):
    i = 0

    date_format_mail = date_amj_to_jma(date)

    message = MIMEMultipart()
    
    destinataire = ['INSERER MAIL']
    message["From"] = 'Alerte Ransomware'
    message["Subject"] = f'Bilan Ransomware - {date_format_mail}'

    if nb_raas == 0:
        msg = f"Depuis début {str(date_aaaa_mm_jj())[:4]}, il y a eu {nb_raas_annee} attaques par ransomware revendiquées\n\nCependant, aujourd'hui aucune attaque n'a été revendiquée le {date_format_mail}."

    else:
        msg = f"<table border: 1px;><thead><tr><th colspan=3>Bilan des {nb_raas} attaques par ransomware du {date_format_mail}</th></tr></thead><tbody>"

        while i < nb_raas:
            #msg += f"<br>{i+1}) Attaquant : {liste_raas[i][1]} | Victime : {liste_raas[i][0]}"

            msg += f"<tr><td border: 1px;>{i+1})</td> <td>Attaquant : {liste_raas[i][1]}</td><td>Victime : {liste_raas[i][0]}</td>"
            i+=1

        msg += "</tbody></table>"

        msg += f"<br>PS : Depuis début {str(date_aaaa_mm_jj())[:4]}, il y a eu {nb_raas_annee} attaques par ransomware revendiquées dans le monde<br><br>Cordialement l'outil de monitoring du pôle IT Alcyconie by Juniors<br>"

    messageText = MIMEText(msg, 'html')

    message.attach(messageText)

    email = 'INSERER MAIL'
    password = 'INSERER MDP'

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo('Gmail')
    server.starttls()
    server.login(email, password)
    fromaddr = email

    for dest in destinataire:
        message["To"] = dest

        server.sendmail(fromaddr, dest, message.as_string())

    server.quit()

if __name__ == '__main__':
    choix = start()
    liste_donnees = scrapping_raas()
    liste_raas, nb_raas, date = tri_tableau(liste_donnees, choix)
    nb_raas_annee = nb_raas_annee_actuelle(liste_donnees)
    affichage_liste(liste_raas, nb_raas, date, nb_raas_annee)
    choix_envoi_mail = choix_mail()
    if choix_envoi_mail == 1:
        envoi_mail(nb_raas, liste_raas, date, nb_raas_annee)

#Ajout dans CaillouNoir
#choix mail : 1) alcyonie all ou autre mail
#Ajout schéma des 10 plus gros groupes de l'année genre camembert
#Ajout nb_raas par groupe sur l'année ou mois
