from difflib import SequenceMatcher

from database import (
    init_db,
    inserer_contact,
    hash_existe,
    lister_contacts,
    enregistrer_rejet,
)
from normalisation import (
    calculer_hash,
    normaliser_nom,
    normaliser_email,
    normaliser_telephone,
)

    # Part: Similarity threshold
SEUIL_SIMILARITE = 0.85

    # Part: Similarity check

def noms_similaires(nom1,nom2):
    n1 = normaliser_nom(nom1)
    n2 = normaliser_nom(nom2)
    return SequenceMatcher(None, n1, n2).ratio() >= SEUIL_SIMILARITE



    # Part: Classify contact

def classifier(nom, email, telephone):
    if hash_existe(calculer_hash(nom, email, telephone)):
        return "redondante"

    email_n = normaliser_email(email)
    tel_n = normaliser_telephone(telephone)
    similaire_trouve = False

    for nom_e , email_e, tel_e in lister_contacts():
        if not noms_similaires(nom, nom_e):
            continue
        similaire_trouve = True
        meme_email = email_n == normaliser_email(email_e)
        meme_tel = tel_n != "" and tel_n == normaliser_telephone(tel_e)
        if meme_email or meme_tel:
            return "redondante"

    if similaire_trouve:
        return "faux_positif"
    return "nouvelle"


    # Part: Process contact

def traiter_contact(nom, email, telephone):
    statut = classifier(nom, email, telephone)
    if statut == "redondante":
        enregistrer_rejet(nom, email, telephone, "doublon détecté")
        return statut
    inserer_contact(nom, email, telephone, calculer_hash(nom, email, telephone))
    return statut


    # Part: Tests

if __name__ == "__main__":
    init_db()
    tests= [
        ("Ahmed Benali", "ahmed@mail.com", "0555123456"),
        ("  ahmed   BENALI ", "AHMED@mail.com", "0555-12-34-56"),
        ("Ahmed Benali", "ahmed.autre@mail.com", "0661000000"),
        ("Sara Khelifi", "sara@mail.com", "0770111222"),
        ("Ahmed Benalli", "ahmed@mail.com", "0555123456"),
    ]
    for nom, email, telephone in tests:
        print(nom.strip(), "->", traiter_contact(nom, email, telephone))

