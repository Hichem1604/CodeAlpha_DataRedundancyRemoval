import csv
import os

import pytest

import database
from database import init_db, inserer_contact, hash_existe, lister_contacts
from normalisation import (
    calculer_hash,
    normaliser_nom,
    normaliser_email,
    normaliser_telephone,
)
from validation import classifier, traiter_contact

FICHIER_CSV = os.path.join(os.path.dirname(__file__), "donnees_test.csv")


@pytest.fixture(autouse=True)
def base_temporaire(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_NAME", str(tmp_path / "test.db"))
    init_db()


def compter_rejets():
    with database.get_connection() as conn:
        return conn.execute("SELECT COUNT(*) FROM rejets").fetchone()[0]


def test_normaliser_nom_enleve_accents_et_espaces():
    assert normaliser_nom("  Hélène   DUPONT ") == "helene dupont"


def test_normaliser_email_minuscules():
    assert normaliser_email("  AHMED@Mail.com ") == "ahmed@mail.com"


def test_normaliser_telephone_garde_les_chiffres():
    assert normaliser_telephone("0555-12 34.56") == "0555123456"
    assert normaliser_telephone(None) == ""


def test_hash_a_64_caracteres():
    assert len(calculer_hash("Ahmed Benali", "ahmed@mail.com", "0555123456")) == 64


def test_hash_identique_pour_le_meme_contact_ecrit_autrement():
    h1 = calculer_hash("Ahmed Benali", "ahmed@mail.com", "0555 12 34 56")
    h2 = calculer_hash("  ahmed   BENALI ", "AHMED@mail.com", "0555-12-34-56")
    assert h1 == h2


def test_hash_different_si_email_different():
    h1 = calculer_hash("Ahmed Benali", "ahmed@mail.com", "0555123456")
    h3 = calculer_hash("Ahmed Benali", "autre@mail.com", "0555123456")
    assert h1 != h3


def test_inserer_puis_doublon_refuse():
    assert inserer_contact("Ahmed Benali", "ahmed@mail.com", "0555123456", "h1") is True
    assert inserer_contact("Ahmed Benali", "ahmed@mail.com", "0555123456", "h1") is False
    assert hash_existe("h1") is True
    assert hash_existe("inconnu") is False


def test_contact_nouveau():
    assert classifier("Ahmed Benali", "ahmed@mail.com", "0555123456") == "nouvelle"


def test_doublon_deguise_est_redondant_et_rejete():
    traiter_contact("Ahmed Benali", "ahmed@mail.com", "0555 12 34 56")
    statut = traiter_contact("  ahmed   BENALI ", "AHMED@mail.com", "0555-12-34-56")
    assert statut == "redondante"
    assert len(lister_contacts()) == 1
    assert compter_rejets() == 1


def test_faute_de_frappe_avec_meme_email_est_redondante():
    traiter_contact("Ahmed Benali", "ahmed@mail.com", "0555123456")
    statut = traiter_contact("Ahmed Benalli", "ahmed@mail.com", "0555123456")
    assert statut == "redondante"
    assert len(lister_contacts()) == 1


def test_meme_nom_autres_coordonnees_est_un_faux_positif_insere():
    traiter_contact("Ahmed Benali", "ahmed@mail.com", "0555123456")
    statut = traiter_contact("Ahmed Benali", "autre@mail.com", "0661000000")
    assert statut == "faux_positif"
    assert len(lister_contacts()) == 2
    assert compter_rejets() == 0


def test_telephone_vide_ne_compte_pas_comme_un_doublon():
    traiter_contact("Sara Khelifi", "sara@mail.com", "")
    statut = traiter_contact("Sara Khelifi", "sara2@mail.com", "")
    assert statut == "faux_positif"


@pytest.mark.skipif(not os.path.exists(FICHIER_CSV), reason="donnees_test.csv introuvable")
def test_precision_sur_le_jeu_de_donnees():
    total = 0
    corrects = 0
    with open(FICHIER_CSV, newline="", encoding="utf-8") as f:
        for ligne in csv.DictReader(f):
            obtenu = traiter_contact(ligne["nom"], ligne["email"], ligne["telephone"])
            total += 1
            if obtenu == ligne["attendu"]:
                corrects += 1
    assert total == 100
    assert corrects / total >= 0.95