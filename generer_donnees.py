import csv
import random
import unicodedata

random.seed(42)


PRENOMS = [
    "Ahmed", "Sara", "Yacine", "Amina", "Karim", "Lina", "Mohamed", "Nadia",
    "Samir", "Hélène", "Walid", "Imane", "Rachid", "Meriem", "Omar", "Fatima",
    "Bilal", "Sofia", "Nabil", "Khadija", "Hichem", "Salima", "Adel", "Rania",
    "Farid", "Zineb", "Anis", "Leila", "Sofiane", "Djamila",
]
NOMS = [
    "Benali", "Khelifi", "Boudiaf", "Mansouri", "Haddad", "Cherif", "Belkacem",
    "Saidi", "Brahimi", "Merabet", "Ziani", "Touati", "Amrani", "Slimani",
    "Bouzid", "Hamidi", "Kaci", "Laribi", "Messaoudi", "Rahmani", "Yahia",
    "Zerrouki", "Ferhat", "Guendouz", "Larbi", "Ouali", "Taleb", "Bensaid",
    "Medjdoub", "Naili",
]


def sans_accents(texte):
    texte = unicodedata.normalize("NFD", texte)
    return "".join(c for c in texte if unicodedata.category(c) != "Mn")


def formater_telephone(numero):
    style = random.choice(["espaces", "tirets", "brut"])
    if style == "espaces":
        return " ".join([numero[:4], numero[4:6], numero[6:8], numero[8:]])
    if style == "tirets":
        return "-".join([numero[:4], numero[4:6], numero[6:8], numero[8:]])
    return numero


def deguiser(nom, email, telephone):
    variante = random.choice(["majuscules", "minuscules", "espaces"])
    if variante == "majuscules":
        nom = nom.upper()
        email = email.upper()
    elif variante == "espaces":
        nom = " "+nom.replace(" ", "  ")+" "
    else:
        nom = nom.lower()
    return nom, email, formater_telephone(telephone)


def faute_de_frappe(nom):
    prenom, nom_famille = nom.split(" ")
    position = random.randrange(1, len(nom_famille) - 1)
    operation = random.choice(["doubler", "supprimer", "remplacer"])
    if operation == "doubler":
        nom_famille = nom_famille[:position] + nom_famille[position] + nom_famille[position:]
    elif operation == "supprimer":
        nom_famille = nom_famille[:position] + nom_famille[position + 1 :]
    else:
        nom_famille = nom_famille[:position] + "x" + nom_famille[position + 1 :]
    return prenom + " " + nom_famille


bases = []
for i, (prenom, nom_famille) in enumerate(zip(PRENOMS, NOMS)):
    nom = prenom + " " + nom_famille
    email = sans_accents(prenom + "." + nom_famille).lower() + "@mail.com"
    telephone = "0555" + str(100000 + i * 7919).zfill(6)
    bases.append((nom, email, telephone))


lignes = [(n, e, t, "nouvelle") for n, e, t in bases]


suite = []
for nom, email, telephone in bases:
    n, e, t =  deguiser(nom, email, telephone)
    suite.append((n, e, t, "redondante"))

for nom, email, telephone in random.sample(bases, 20):
    suite.append((faute_de_frappe(nom), email, formater_telephone(telephone), "redondante"))

for index, (nom, email, telephone) in enumerate(random.sample(bases, 20)):
    nouvel_email = email.replace("@", ".pro@")
    nouveau_tel = "0661" + str(200000 + index * 3571).zfill(6)
    suite.append((nom, nouvel_email, nouveau_tel, "faux_positif"))


random.shuffle(suite)
lignes += suite

with open("donnees_test.csv", "w", newline="",encoding="utf_8") as f:
    writer = csv.writer(f)
    writer.writerow(["nom", "email", "telephone", "attendu"])
    writer.writerows(lignes)

print(len(lignes), "lignes écrites dans donnees_test.csv")