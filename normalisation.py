import hashlib
import re
import unicodedata

    # Part: Data normalization

def normaliser_nom(nom):
    nom = nom.strip().lower()
    nom = unicodedata.normalize("NFD", nom)
    nom = "".join(c for c in nom if unicodedata.category(c) != "Mn")
    nom = re.sub(r"[^a-z0-9]+", " ", nom)
    return nom.strip()


def normaliser_email(email):
    return email.strip().lower()


def normaliser_telephone(telephone):
    return re.sub(r"\D", "", telephone or "")


    # Part: Calculate hash

def calculer_hash(nom, email, telephone):
    cle = "|".join([
        normaliser_nom(nom),
        normaliser_email(email),
        normaliser_telephone(telephone),
    ])
    return hashlib.sha256(cle.encode("utf-8")).hexdigest()


    # Part: Tests

if __name__ == "__main__":
    h1 = calculer_hash("Ahmed Benali", "ahmed@mail.com", "0555 12 34 56")
    h2 = calculer_hash("  ahmed   BENALI ", "AHMED@mail.com", "0555-12-34-56")
    h3 = calculer_hash("Ahmed Benali", "autre@mail.com", "0555 12 34 56")
    h4 = calculer_hash("Ahmed Benali", "ahmed@mail.com", "0555123456")
    print(h1)
    print(h1 == h2)
    print(h1 == h3)
    print(h1==h4)