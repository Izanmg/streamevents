## StreamEvents

Aplicació desenvolupada amb **Django** per gestionar esdeveniments i usuaris.
El projecte està pensat com una base sòlida i extensible amb bones pràctiques de desenvolupament:
configuració d'entorns, separació de plantilles i fitxers estàtics, estructura modular i ús de fitxers `.env`.
Opcionalment, es pot integrar amb **MongoDB** mitjançant **Djongo** en fases posteriors.

---

## ✨ Objectius

* Practicar un projecte **Django modular** i escalable.
* Treballar amb un **usuari personalitzat** (app `users`).
* Organitzar correctament **templates**, **estàtics** i **media**.
* Introduir fitxers d’entorn (`.env`) i bones pràctiques amb **Git**.
* Preparar la base per a **futures funcionalitats**: API, autenticació avançada, etc.

---

## 🧱 Stack Principal

* **Python 3.10+**
* **Django 5.x**
* **SQLite3** (per defecte)
* **Djongo + MongoDB** *(opcional)*
* **HTML / CSS / JS** (per a la capa de presentació)
* **dotenv** per a la gestió d’entorns

---

## 📂 Estructura Simplificada

```
streamevents/
├── manage.py
├── streamevents/          # Configuració principal (settings, urls, wsgi)
├── users/                 # App personalitzada d'usuaris
├── events/                # App per a esdeveniments
│
├── templates/             # Plantilles globals (base.html, layouts, etc.)
├── static/                # CSS, JS i imatges pròpies
├── media/                 # Fitxers pujats per l'usuari (NO es puja a Git)
│
├── fixtures/              # (opcional) JSON de dades d’exemple
├── seeds/                 # (opcional) Scripts Python per omplir dades
│
├── requirements.txt       # Dependències del projecte
├── .env                   # Variables d’entorn (privat)
├── env.example            # Exemple públic sense secrets
├── README.md              # Documentació del projecte
└── .gitignore             # Arxius a ignorar pel control de versions
```

---

## ✅ Requisits previs

Abans de començar, assegura’t de tenir instal·lat:

* **Python 3.10 o superior**
* **pip**
* **Virtualenv** (opcional però recomanat)
* **Git**

---

## 🚀 Instal·lació ràpida

```bash
# 1️⃣ Clona el repositori
git clone https://github.com/usuari/streamevents.git
cd streamevents

# 2️⃣ Crea i activa l'entorn virtual
python -m venv env
source env/bin/activate   # Linux/Mac
env\Scripts\activate      # Windows

# 3️⃣ Instal·la les dependències
pip install -r requirements.txt

# 4️⃣ Configura el fitxer .env
cp env.example .env

# 5️⃣ Executa les migracions inicials
python manage.py migrate

# 6️⃣ Inicia el servidor
python manage.py runserver
```

---

## 🔐 Variables d'entorn (env.example)

Exemple de contingut del fitxer `.env`:

```
DEBUG=True
SECRET_KEY=canvia_aqui_la_teva_clau_secreta
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## 👤 Superusuari

Per crear un compte d’administrador:

```bash
python manage.py createsuperuser
```

Després accedeix al **panell d’administració** a:
👉 `http://localhost:8000/admin/`

---

## 🗃️ Migrar a MongoDB (opcional futur)

Per utilitzar **MongoDB** com a base de dades:

1. Instal·la Djongo:

   ```bash
   pip install djongo
   ```
2. Modifica la configuració de la base de dades a `settings.py`:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'djongo',
           'NAME': 'streamevents_db',
       }
   }
   ```
3. Aplica noves migracions:

   ```bash
   python manage.py migrate
   ```

---

## 🛠️ Comandes útils

```bash
python manage.py runserver       # Executar el servidor
python manage.py makemigrations  # Crear migracions
python manage.py migrate         # Aplicar migracions
python manage.py createsuperuser # Crear superusuari
python manage.py shell           # Obtenir shell interactiu
```

---

## 💾 Fixtures (exemple)

Fitxer `fixtures/grups.json`:

```json
[
  { "model": "auth.group", "fields": { "name": "Administradors" } },
  { "model": "auth.group", "fields": { "name": "Usuaris" } }
]
```

Carrega’l amb:

```bash
python manage.py loaddata fixtures/grups.json
```

---

## 🌱 Seeds (exemple d'script)

Fitxer `seeds/init_data.py`:

```python
from users.models import CustomUser

def run():
    CustomUser.objects.create_user(
        username="demo",
        email="demo@streamevents.com",
        password="demo123"
    )
    print("Usuari de prova creat amb èxit.")
```

Executa’l amb:

```bash
python manage.py shell < seeds/init_data.py
```
