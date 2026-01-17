# Carlsberg Koprivnica – User Management App (PostgreSQL + Django Admin)

Tema: Upravljanje korisničkim računima (vrste korisnika, prava pristupa, metapodaci) uz PostgreSQL (objektno-relacijski DB) i web GUI.

## Tehnologije
- PostgreSQL
- Django (Python)
- Django Admin (GUI)

## Pokretanje (Windows)
1. Instalirati PostgreSQL i osigurati da `psql` radi u terminalu.
2. Pokrenuti:
   - `install.bat`

## Funkcionalnosti
- Upravljanje korisnicima i grupama (role/permissions)
- Metapodaci korisnika preko JSONB (UserProfile.metadata)
- Audit log u PostgreSQL (okidači/triggeri) + changed_by iz middlewarea (SET LOCAL / set_config)
- VIEW `v_user_effective_permissions`
- FUNCTION `has_permission(...)`

## GitHub
Repo: https://github.com/jpobi22/TBP-User-Managment-App.git

## Demo (seed)
Lozinka za seed korisnike: `Carlsberg123!`
Primjeri: `it.admin`, `hr.maria`, `ro.auditor`

## Rute
/ (index), /training/, /it/, /hr/, /sales/, /audit/, /admin
