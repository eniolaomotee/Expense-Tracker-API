# Expense-Tracker-API
This API allows users to create, read, update, and delete expenses. Users can also filter their expenses based on months and categories.

📌 [Project Roadmap Source](https://roadmap.sh/projects/expense-tracker-api)

---

## 🚀 Features
- ✅ User Registration & JWT Login
- ✅ Create, Read, Update, and Delete Expenses
- 🔍 Filter Expenses by Category or Date (optional for future)
- 📊 Expense Category Enumeration (e.g., food, transport, clothing, etc.)
- 🧪 Unit & Integration Tests using pytest and SQLite
- 🧰 Production-ready with Supabase PostgreSQL
---

## 🛠️ Tech Stack

- **Backend Framework**: FastAPI
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Auth**: JWT (JSON Web Tokens)
- **Database**: SQLite (testing), Supabase PostgreSQL (production)
- **Testing**: Pytest, httpx, pytest-asyncio
- **Deployment**: None(for now)

---

## 📦 Installation

1. Clone the repository

```bash
git clone https://github.com/your-username/expense-tracker-api.git
cd expense-tracker-api
```

2. Create and activate a Virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
DATABASE_URL=sqlite:///./test.db  # or your Supabase URL
SECRET_KEY=your-secret
ALGORITHM=your-algorithm-key
```

5. Running Tests
``` bash
pytest
```



### This project is licensed under the MIT License.
