# cooking-recipes-app
Web application for Searching and managing cooking recipes

These are instructions to hopefully set this up correctly:

## 🚀 Getting Started

### Prerequisites
- Node.js & npm
- Python 3.x
- PostgreSQL

---

### 1. Clone the Repo
```bash
git clone https://github.com/Ashanth-Ganesh/cooking-recipes-app
cd cooking-recipes-app
```

---

### 2. Backend Setup
```bash
cd server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the `server/` directory (spoonacular_api_key can be found in the microsoft teams Group chat will have to scroll up a bit tho):
```env
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=your_db_name
SPOONACULAR_API_KEY=your_spoonacular_api_key
```

> Get a free Spoonacular API key at [spoonacular.com/food-api](https://spoonacular.com/food-api)

**Set up PostgreSQL:**
```bash
sudo dnf install postgresql postgresql-server   # Fedora
sudo postgresql-setup --initdb
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

Create the database and user:
```bash
sudo -u postgres psql
```
```sql
CREATE USER your_db_user WITH PASSWORD 'your_db_password';
CREATE DATABASE your_db_name OWNER your_db_user;
\q
```

Then in `/var/lib/pgsql/data/pg_hba.conf`, make sure these lines use `md5`:
```
host    all    all    127.0.0.1/32    md5
host    all    all    ::1/128         md5
```
```bash
sudo systemctl restart postgresql
```

Start the server:
```bash
uvicorn app:app --reload
```
Server runs at `http://127.0.0.1:8000`

---

### 3. Frontend Setup
```bash
cd client/recipes-app-ui
npm install
npm start
```
App runs at `http://localhost:4200`