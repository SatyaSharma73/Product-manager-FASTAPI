<div align="center">

# 🛒 Product Manager

**A full-stack product management application built with FastAPI, MySQL, and React**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.x-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![i18n](https://img.shields.io/badge/i18n-EN%20%7C%20HI%20%7C%20FR%20%7C%20ES-blueviolet?style=for-the-badge)](https://react.i18next.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red?style=for-the-badge)](https://www.sqlalchemy.org/)
[![Axios](https://img.shields.io/badge/Axios-HTTP-5A29E4?style=for-the-badge)](https://axios-http.com/)

</div>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Architecture](#-architecture)
- [Database Schema](#-database-schema)
- [API Reference](#-api-reference)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Running the App](#-running-the-app)
- [UI Walkthrough](#-ui-walkthrough)
- [Screenshots](#-screenshots)
- [Internationalization](#-internationalization)
- [Excel Import & Export](#-excel-import--export)
- [Bug Fixes](#-bug-fixes)

---

## 🔍 Overview

**Product Manager** is a full-stack CRUD application that lets you manage a product catalogue through a clean, modern React dashboard. The backend is powered by **FastAPI** with a **MySQL** database via **SQLAlchemy ORM**, and the frontend is a **Create React App** project that communicates with the API over HTTP.

Each product has a name, description, price, and active/inactive status. The dashboard gives you real-time statistics, powerful filtering, sorting, inline editing, bulk operations, Excel import/export, a language switcher with 4 languages, and dark mode — all in one place.

---

## 🧰 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Backend** | FastAPI | REST API framework |
| **ORM** | SQLAlchemy | Database abstraction |
| **Validation** | Pydantic v2 | Request / response schemas |
| **Database** | MySQL 8+ | Persistent data storage |
| **DB Driver** | PyMySQL | Python → MySQL connector |
| **Excel (backend)** | openpyxl | Parse uploaded `.xlsx` files, generate template |
| **File upload** | python-multipart | Handle `multipart/form-data` in FastAPI |
| **Frontend** | React 19 (CRA) | UI framework |
| **HTTP Client** | Axios | API calls from React |
| **Excel (frontend)** | SheetJS (`xlsx`) | Client-side Excel export |
| **i18n** | react-i18next + i18next | Internationalisation, 4 languages |
| **Lang detection** | i18next-browser-languagedetector | Auto-detect language from browser / localStorage |
| **Styling** | Pure CSS (CSS Variables) | Theming, dark mode |
| **Dev Runner** | concurrently | Run API + UI with one command |

---

## ✨ Features

### Dashboard
- **Live stats sidebar** — Total, Active, Inactive counts + Average Price + Total Catalogue Value
- **Clickable stat cards** — click Total / Active / Inactive to filter the table instantly
- **Dark mode** — toggle between light and dark themes; preference persists across sessions
- **Language switcher** — switch between 🇬🇧 English, 🇮🇳 Hindi, 🇫🇷 French, 🇪🇸 Spanish from the navbar

### Products Table
| Feature | Details |
|---|---|
| **Search** | Filter by product name or description in real time |
| **Date filter** | Filter products by creation date range |
| **Price filter** | Filter by minimum and/or maximum price |
| **Sort** | Click column headers (Name, Price, Created) to sort asc/desc |
| **Status toggle** | Click Active / Inactive badge directly in the row to flip status instantly |
| **Hover preview** | Hover over a product name to see a floating card with full details |
| **Copy UUID** | Click any Product ID cell to copy it to clipboard |
| **Row selection** | Checkbox per row + select-all for bulk operations |
| **Bulk delete** | Select multiple products and delete them in one click |
| **Export to Excel** | Download all visible (filtered) rows as `.xlsx` — import-compatible format |
| **Export selected** | Download only the checked rows as `.xlsx` |
| **Edit** | Open a pre-filled modal to update any product field |
| **Delete** | Delete a single product with a confirmation modal |

### Import Excel
| Step | Details |
|---|---|
| **Drop zone** | Drag & drop or click-to-browse for `.xlsx` / `.xls` files |
| **Preview** | See all rows parsed from the file before any data is written |
| **Row selection** | Check/uncheck individual rows; invalid rows are disabled automatically |
| **Validation** | Backend validates name and price; invalid rows are highlighted with a reason |
| **Selective import** | Only the rows you select are inserted into the database |
| **Template download** | Download a pre-formatted `.xlsx` template to fill in |

### Other Pages
- **Add Product** — Form to create a new product with name, description, price, and status
- **Find by ID** — Look up any product instantly by its UUID with specific error messages for 404 / invalid format / server down

---

## 📁 Project Structure

```
FastAPI/
│
├── main.py                  # FastAPI app — 9 endpoints (CRUD + import + export)
├── database.py              # SQLAlchemy engine, session, Base
├── db_models.py             # ORM model — ProductORM table
├── model.py                 # Pydantic schemas (Product, ProductCreate,
│                            #   ProductUpdate, ProductPreviewRow, PreviewResponse)
│
├── .env                     # DB credentials (not committed)
├── .gitignore
├── package.json             # Root — runs both servers via `concurrently`
├── requirements.txt         # Python dependencies
│
├── myenv/                   # Python virtual environment (not committed)
│
└── frontend/                # React application (Create React App)
    ├── public/
    │   └── index.html
    └── src/
        ├── App.js           # Root — tabs, theme, language switcher, sidebar stats
        ├── App.css          # All styles: CSS variables, dark mode, i18n switcher
        ├── index.js         # Entry point — imports i18n before React renders
        ├── index.css        # Global reset + font
        │
        ├── i18n/
        │   ├── index.js              # i18next config, language detection
        │   └── locales/
        │       ├── en.json           # English translations
        │       ├── hi.json           # Hindi translations
        │       ├── fr.json           # French translations
        │       └── es.json           # Spanish translations
        │
        ├── api/
        │   └── productApi.js         # Axios wrapper — all API calls
        │
        ├── utils/
        │   └── format.js             # Currency (INR) + date formatters
        │
        └── components/
            ├── ProductsTab.js        # Main table with all features
            ├── AddProductTab.js      # Add product form
            ├── ImportTab.js          # Excel import: drop → preview → import
            ├── FindByIdTab.js        # UUID lookup page
            ├── EditModal.js          # Edit product modal
            └── DeleteModal.js        # Delete confirmation modal
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        BROWSER                               │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐  │
│   │                  React Frontend                      │  │
│   │                 localhost:3000                       │  │
│   │                                                     │  │
│   │  App.js ──► ProductsTab  ──► EditModal              │  │
│   │          ├─► AddProductTab    DeleteModal           │  │
│   │          ├─► ImportTab                              │  │
│   │          └─► FindByIdTab                            │  │
│   │                   │                                 │  │
│   │       productApi.js (Axios)  ·  SheetJS (export)   │  │
│   │       react-i18next (i18n)                         │  │
│   └───────────────────┼─────────────────────────────────┘  │
└───────────────────────┼─────────────────────────────────────┘
                        │ HTTP (proxied in dev)
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend                            │
│                  localhost:8000                              │
│                                                             │
│   main.py                                                   │
│   ├── GET    /getallproducts                                │
│   ├── GET    /getproductbyid/{id}                           │
│   ├── POST   /addproduct                                    │
│   ├── PUT    /updateproduct/{id}                            │
│   ├── DELETE /deleteproduct/{id}                            │
│   ├── GET    /importtemplate      ← download .xlsx template │
│   ├── POST   /previewimport       ← parse + validate file   │
│   ├── POST   /importselected      ← bulk insert chosen rows │
│   └── POST   /importproducts      ← legacy file import      │
│                   │                                         │
│      SQLAlchemy ORM · openpyxl · python-multipart           │
│            database.py                                      │
└───────────────────┼─────────────────────────────────────────┘
                    │ PyMySQL
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                  MySQL Database                              │
│                                                             │
│   Table: products                                           │
│   ┌──────────────┬──────────────────────────────────────┐  │
│   │ id           │ VARCHAR(36) PRIMARY KEY (UUID)        │  │
│   │ name         │ VARCHAR(200) NOT NULL                 │  │
│   │ description  │ TEXT NULLABLE                         │  │
│   │ price        │ FLOAT NOT NULL                        │  │
│   │ is_active    │ BOOLEAN DEFAULT TRUE                  │  │
│   │ created_at   │ DATETIME                              │  │
│   │ updated_at   │ DATETIME                              │  │
│   └──────────────┴──────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗄️ Database Schema

```sql
CREATE TABLE products (
    id          VARCHAR(36)  NOT NULL PRIMARY KEY,   -- UUID string
    name        VARCHAR(200) NOT NULL,
    description TEXT,
    price       FLOAT        NOT NULL,
    is_active   BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at  DATETIME     NOT NULL,
    updated_at  DATETIME     NOT NULL
);
```

> The table is auto-created on startup via `Base.metadata.create_all(bind=engine)` — no manual migration needed.

---

## 📡 API Reference

Base URL: `http://localhost:8000`

### `GET /getallproducts`
Returns all products in the database.

**Response `200`**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Wireless Headphones",
    "description": "Noise cancelling over-ear headphones",
    "price": 3499.99,
    "is_active": true,
    "created_at": "2025-05-10T10:30:00",
    "updated_at": "2025-05-10T10:30:00"
  }
]
```

---

### `GET /getproductbyid/{id}`
Find a single product by its UUID.

| Parameter | Type | Description |
|---|---|---|
| `id` | `UUID` | Product UUID |

**Response `200`** — Product object  
**Response `404`** — `{"detail": "Product not found"}`

---

### `POST /addproduct`
Create a new product.

**Request Body**
```json
{
  "name": "Wireless Headphones",
  "description": "Optional description",
  "price": 3499.99,
  "is_active": true
}
```

| Field | Type | Required | Constraints |
|---|---|---|---|
| `name` | string | ✅ | max 200 chars |
| `description` | string | ❌ | max 1000 chars |
| `price` | float | ✅ | must be > 0 |
| `is_active` | boolean | ❌ | default: `true` |

**Response `200`** — Created product with generated `id`, `created_at`, `updated_at`

---

### `PUT /updateproduct/{id}`
Partially update an existing product. Only send the fields you want to change.

**Request Body** (all fields optional)
```json
{
  "name": "Updated Name",
  "price": 2999.00,
  "is_active": false
}
```

**Response `200`** — Updated product object  
**Response `404`** — `{"detail": "Product not found"}`

---

### `DELETE /deleteproduct/{id}`
Permanently delete a product.

**Response `200`**
```json
{ "message": "Product 'Wireless Headphones' deleted successfully" }
```
**Response `404`** — `{"detail": "Product not found"}`

---

### `GET /importtemplate`
Download a pre-formatted `.xlsx` template with correct column headers, ready to fill in and re-upload.

**Response `200`** — `products_template.xlsx` (binary stream)

---

### `POST /previewimport`
Parse and validate an uploaded Excel file. **No data is written to the database.** Returns a preview of every row with validity flags.

**Request** — `multipart/form-data` with field `file` (`.xlsx` or `.xls`)

**Response `200`**
```json
{
  "total": 5,
  "valid_count": 4,
  "rows": [
    {
      "row_num": 2,
      "name": "Wireless Headphones",
      "description": "Noise cancelling",
      "price": 3499.99,
      "is_active": true,
      "valid": true,
      "reason": null
    },
    {
      "row_num": 3,
      "name": null,
      "description": null,
      "price": null,
      "is_active": true,
      "valid": false,
      "reason": "Name is required"
    }
  ]
}
```

---

### `POST /importselected`
Bulk insert a list of products chosen from the preview. Accepts only pre-validated rows sent as JSON.

**Request Body**
```json
[
  { "name": "Headphones", "description": "...", "price": 3499.99, "is_active": true },
  { "name": "Keyboard",   "description": null,  "price": 1299.00, "is_active": true }
]
```

**Response `200`**
```json
{ "imported": 2 }
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- [Python 3.10+](https://www.python.org/downloads/)
- [Node.js 18+ & npm](https://nodejs.org/)
- [MySQL 8.0+](https://dev.mysql.com/downloads/)
- [Git](https://git-scm.com/)

---

### 1. Clone the repository

```bash
git clone https://github.com/SatyaSharma73/Product-manager-FASTAPI.git
cd Product-manager-FASTAPI
```

---

### 2. Set up the Python backend

```bash
# Create and activate virtual environment
python -m venv myenv

# Windows
myenv\Scripts\activate

# macOS / Linux
source myenv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

### 3. Set up the React frontend

```bash
# Install root dev tools (concurrently)
npm install

# Install React dependencies
cd frontend
npm install --legacy-peer-deps
cd ..
```

> `--legacy-peer-deps` is required because `react-i18next` and `i18next` have a peer dependency on TypeScript ≥ 5, while Create React App ships TypeScript 4.

---

### 4. Set up the database

Create a database in MySQL:

```sql
CREATE DATABASE productdb;
```

> The `products` table will be created automatically when the backend starts.

---

## 🔑 Environment Variables

Create a `.env` file in the **project root** (same folder as `main.py`):

```env
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=productdb
```

> ⚠️ Never commit `.env` to version control. It is already listed in `.gitignore`.

---

## ▶️ Running the App

### Option A — Run both servers with one command (recommended)

```bash
npm run dev
```

This starts both the FastAPI backend and the React frontend simultaneously using `concurrently`.

---

### Option B — Run servers separately

**Terminal 1 — Backend**
```bash
myenv\Scripts\activate          # Windows
# source myenv/bin/activate     # macOS/Linux
uvicorn main:app --reload
```

**Terminal 2 — Frontend**
```bash
cd frontend
npm start
```

---

### Access the app

| Service | URL |
|---|---|
| **React App** | http://localhost:3000 |
| **FastAPI** | http://localhost:8000 |
| **API Docs (Swagger)** | http://localhost:8000/docs |
| **API Docs (Redoc)** | http://localhost:8000/redoc |

---

## 🖥️ UI Walkthrough

### Dashboard Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  PM  Product Manager · FastAPI · MySQL  [🌐 EN▾]  [🌙]          │
├──────────────────────────────────────────────┬───────────────────┤
│                                              │  ┌─────────────┐  │
│  [Active Products][Add Product]              │  │ 🟦 Total 12 │  │
│  [Import Excel]  [Find by ID]                │  ├─────────────┤  │
│                                              │  │ ✅ Active 9 │  │
│  ┌────────────────────────────────────────┐  │  ├─────────────┤  │
│  │ Products 9  [search…] From[date]To[date│  │  │ ❌ Inact. 3 │  │
│  │ Min₹[   ] Max₹[   ]  [Export Excel]   │  │  ├─────────────┤  │
│  │ [Refresh]                              │  │  │ ₹ Avg Price │  │
│  ├──┬──┬────────┬──────────┬──────┬──────┤  │  ├─────────────┤  │
│  │☐ │# │ID      │Name      │Price │...   │  │  │ 💼 Total Val│  │
│  ├──┼──┼────────┼──────────┼──────┼──────┤  │  └─────────────┘  │
│  │  │  │        │          │      │      │  │                    │
│  └──┴──┴────────┴──────────┴──────┴──────┘  │                    │
└──────────────────────────────────────────────┴───────────────────┘
```

### Tab Pages

| Tab | Description |
|---|---|
| **Active Products** | Shows only `is_active = true` products with full filter/sort/export |
| **Add Product** | Form with name, description, price, status fields |
| **Import Excel** | 3-step flow: drop file → preview rows → import selected |
| **Find by ID** | Paste a UUID to fetch and display a single product |
| *(sidebar click)* **Total Products** | Shows all products (active + inactive) |
| *(sidebar click)* **Inactive** | Shows only `is_active = false` products |

---

## 📸 Screenshots

### 🌤️ Dashboard — Light Mode
> The main product table with search, filters, sort, status toggle, and sidebar stats in light theme.

![Dashboard Light Mode](screenshots/dashboard-light.png)

---

### 🌙 Dashboard — Dark Mode
> The same dashboard with the dark theme enabled. Preference is saved automatically across sessions.

![Dashboard Dark Mode](screenshots/dashboard-dark.png)

---

### ➕ Add Product
> The Add Product tab with a clean form for entering product name, description, price, and active status.

![Add Product](screenshots/add-product.png)

---

## 🌍 Internationalization

The entire UI is fully translated into **4 languages**. Language selection is persisted in `localStorage` and auto-detected from the browser on first visit.

| Flag | Language | Code | Native name |
|---|---|---|---|
| 🇬🇧 | English | `en` | English |
| 🇮🇳 | Hindi | `hi` | हिन्दी |
| 🇫🇷 | French | `fr` | Français |
| 🇪🇸 | Spanish | `es` | Español |

### How it works

```
frontend/src/i18n/
├── index.js              # Configures i18next with localStorage detection
└── locales/
    ├── en.json           # ~190 keys: nav, tabs, stats, table, modals, import…
    ├── hi.json
    ├── fr.json
    └── es.json
```

- Every string in the app calls `t('key')` from `useTranslation()`
- Pluralisation uses `_one` / `_other` suffixes (e.g. `"1 product selected"` vs `"3 products selected"`)
- The **LangSwitcher** in the navbar shows a real country flag image (from `flagcdn.com`), the language name in full, and a code badge — no broken emoji on Windows

### Packages

```bash
npm install react-i18next i18next i18next-browser-languagedetector --legacy-peer-deps
```

---

## 📊 Excel Import & Export

### Export to Excel
Click **Export Excel** in the Products table toolbar to download all currently visible (filtered + sorted) rows as `products.xlsx`.  
Select specific rows first to use **Export Excel (n)** from the bulk action bar — exports only those rows.

The exported file uses **import-compatible column headers** (`name`, `description`, `price`, `is_active`) so it can be re-uploaded directly.

### Import from Excel

The import tab follows a **3-step flow** with no risk of accidental data insertion:

```
Step 1 — Drop Zone          Step 2 — Preview Table      Step 3 — Done
┌────────────────────┐      ┌──────────────────────┐    ┌──────────────┐
│  Drop .xlsx here   │      │ ☑ Row 2  Headphones  │    │ ✅ Import    │
│  or click to browse│  ──► │ ☑ Row 3  Keyboard    │ ──►│    complete! │
│  [Download Template│      │ ✗ Row 4  (no name)   │    │ 3 products   │
│   ]                │      │ ☑ Row 5  Mouse       │    │ added.       │
└────────────────────┘      └──────────────────────┘    └──────────────┘
                             [Import Selected (2)]
```

1. **Upload** — drag & drop or browse for an `.xlsx` / `.xls` file
2. **Preview** — backend parses the file and returns each row with a `valid` flag; no data is saved yet
3. **Select & Import** — check the rows you want; click **Import Selected** to insert only those rows

#### Required Excel columns

| Column | Required | Notes |
|---|---|---|
| `name` | ✅ | Product name, max 200 chars |
| `price` | ✅ | Positive number |
| `description` | ❌ | Optional |
| `is_active` | ❌ | `TRUE` / `FALSE`, defaults to `TRUE` |

> Download the **template** from the Import tab to get a correctly formatted starter file.

### Backend packages

```bash
pip install openpyxl python-multipart
```

---

## 🐛 Bug Fixes

The following bugs were identified and fixed during development:

| # | File | Severity | Issue | Fix |
|---|---|---|---|---|
| 1 | `EditModal.js` | 🔴 Critical | Spinner stuck forever after a failed save — `setLoading(false)` was only in `catch`, not `finally` | Moved `setLoading(false)` to `finally` block |
| 2 | `DeleteModal.js` | 🔴 Critical | Same stuck-spinner issue as EditModal | Same `finally` block fix |
| 3 | `FindByIdTab.js` | 🟡 Medium | All errors showed the same generic message regardless of HTTP status | Added UUID regex pre-validation + specific messages for 404, 422, and network errors |
| 4 | `ImportTab.js` | 🟡 Medium | Uploading an empty Excel file (header row only) showed a blank preview with no feedback | Added `rows.length === 0` guard before entering preview step |
| 5 | `ProductsTab.js` | 🟡 Medium | Typing non-numeric characters in the price filter caused `NaN` comparison errors | Added `!isNaN(parseFloat(value))` guard before price comparisons |

---

## 📦 Python Dependencies

```
fastapi
uvicorn[standard]
sqlalchemy
pymysql
pydantic
python-dotenv
openpyxl
python-multipart
```

Generate / update `requirements.txt`:
```bash
pip freeze > requirements.txt
```

---

## 🔒 Security Notes

- `.env` is excluded from git via `.gitignore` — never expose database credentials
- CORS is configured to only allow `http://localhost:3000` — update for production deployments
- All UUIDs are generated server-side with `uuid4()` — no sequential IDs exposed
- Uploaded Excel files are parsed in-memory — no files are written to disk on the server

---

## 🛠️ Possible Enhancements

- [ ] Pagination for large product lists
- [ ] Image upload per product
- [ ] User authentication (JWT)
- [ ] Product categories / tags
- [ ] Deploy to cloud (Railway, Render, Vercel)
- [ ] Unit & integration tests
- [ ] More languages (German, Japanese, Arabic + RTL support)
- [ ] PDF export

---

## 👤 Author

**Satya Sharma**  
Cognizant Technology Solutions  

---

<div align="center">
  <sub>Built with FastAPI · React · MySQL · i18next · SheetJS</sub>
</div>
