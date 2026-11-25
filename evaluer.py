import csv
import os
from collections import Counter

import database
from database import init_db
from validation import traiter_contact


def evaluer(fichier="donnees_test.csv"):
    if os.path.exists(database.DB_NAME):
        os.remove(database.DB_NAME)
    init_db()

    total = 0
    corrects = 0
    attendus = Counter()
    trouves_justes = Counter()
    erreurs = []

    with open(fichier, newline="", encoding="utf-8") as f:
        for ligne in csv.DictReader(f):
            obtenu = traiter_contact(ligne["nom"], ligne["email"], ligne["telephone"])
            attendu = ligne["attendu"]
            total += 1
            attendus[attendu] += 1
            if obtenu == attendu:
                corrects += 1
                trouves_justes[attendu] += 1
            else:
                erreurs.append((ligne["nom"], attendu, obtenu))

    print("Lignes traitées :", total)
    print("Bonnes classifications :", corrects)
    print("Précision globale : {:.1f} %".format(100 * corrects / total))
    print()
    for categorie in ["nouvelle", "redondante", "faux_positif"]:
        print(categorie, ":", trouves_justes[categorie], "/", attendus[categorie])
    if erreurs:
        print()
        print("Erreurs :")
        for nom, attendu, obtenu in erreurs:
            print(" -", nom.strip(), "| attendu :", attendu, "| obtenu :", obtenu)


if __name__ == "__main__":
    evaluer()