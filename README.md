# CodeAlpha_DataRedundancyRemoval

Data redundancy removal system for a database. Task 1 of the CodeAlpha Cloud Computing internship.

## Overview

Before a new record is added to the database, the system checks it against the existing data, classifies it, and appends only unique and verified entries. Redundant records are rejected and logged with the reason.

## How it works

```
New contact -> normalization -> SHA-256 hash -> hash lookup
            -> similarity check -> classification -> insert or reject
```

**Normalization**: names are lowercased, stripped of extra spaces, accents and punctuation. Emails are lowercased. Phone numbers keep digits only. This way, `"  ahmed   BENALI "` and `"Ahmed Benali"` produce the same fingerprint.

**Classification**:

| Status | Meaning | Action |
|---|---|---|
| `nouvelle` (new) | No similar contact exists | Inserted |
| `redondante` (redundant) | Same hash, or a similar name with the same email or phone | Rejected and logged in the `rejets` table |
| `faux_positif` (false positive) | Similar name but different email and phone: a different person | Inserted after verification |

**Safety layers**: a `UNIQUE` constraint on the hash column makes the database itself refuse exact duplicates, and all SQL queries are parameterized to prevent SQL injection.

## Project structure

```
database.py          SQLite database: tables, insertion, lookups, rejection log
normalisation.py     Normalization and SHA-256 hashing
validation.py        Classification logic and contact processing
generer_donnees.py   Generates a 100-contact test dataset (donnees_test.csv)
evaluer.py           Runs the dataset through the system and reports accuracy
test_systeme.py      Automated tests (pytest)
requirements.txt     Dependencies
```

## Installation

```bash
git clone https://github.com/<your-username>/CodeAlpha_DataRedundancyRemoval.git
cd CodeAlpha_DataRedundancyRemoval
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
```

On macOS/Linux, activate the environment with `source venv/bin/activate`.

## Usage

Run a quick demo:

```bash
python validation.py
```

Expected output:

```
Ahmed Benali -> nouvelle
ahmed   BENALI -> redondante
Ahmed Benali -> faux_positif
Sara Khelifi -> nouvelle
Ahmed Benalli -> redondante
```

Generate the test dataset and measure accuracy:

```bash
python generer_donnees.py
python evaluer.py
```

Run the automated tests:

```bash
python -m pytest -v
```

## Evaluation

The test dataset contains 100 contacts, each with its expected answer:

- 30 new contacts
- 30 redundant contacts written differently (case, spaces, phone format)
- 20 redundant contacts with a typo in the name
- 20 false positives (same name, different email and phone)

The system classifies all 100 contacts correctly. This dataset is synthetic and built around the system's rules, so real-world data may give lower accuracy.

## Limitations

- Two different people with the same name and the same phone number would be flagged as redundant.
- The name similarity threshold is `0.85` (`SEUIL_SIMILARITE` in `validation.py`) and may need tuning on real data.
- The database is currently a local SQLite file.

## Roadmap

- [x] Local SQLite database with a unique constraint
- [x] Normalization and hashing
- [x] Validation and classification (new, redundant, false positive)
- [x] Test dataset, accuracy evaluation and pytest tests
- [ ] Migration to a cloud database (AWS RDS, Google Cloud SQL or Azure SQL)
- [ ] Efficiency improvements (index on the hash column, batch inserts)
- [ ] Project explanation video

## Author

CodeAlpha Cloud Computing Internship, Task 1.