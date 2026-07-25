# FastAPI CRUD - Stationary Store (In-Memory Database)
**Complete Setup Guide - From Opening VS Code to Running Your API**

---

# TABLE OF CONTENTS
1. [Prerequisites](#prerequisites)
2. [Phase 1: Environment Setup](#phase-1-environment-setup)
3. [Phase 2: Create Project Files](#phase-2-create-project-files)
4. [Phase 3: Run Your API](#phase-3-run-your-api)
5. [Phase 4: Test Everything](#phase-4-test-everything)
6. [Troubleshooting](#troubleshooting)

---

# PREREQUISITES

Before starting:
- ✅ Python 3.8+ installed
- ✅ VS Code installed
- ✅ A folder on Desktop called `fastapi`

---

---

# PHASE 1: ENVIRONMENT SETUP

## STEP 1: Open VS Code

1. Click VS Code icon
2. VS Code opens

✅ **Expected:** VS Code window is open

---

## STEP 2: Open Your Project Folder

1. **File** → **Open Folder**
2. Navigate to Desktop
3. Select folder: `fastapi`
4. **Click "Select Folder"**

✅ **Expected:** Left sidebar shows "FASTAPI" folder (empty)

---

## STEP 3: Open Terminal

1. **Terminal** menu → **New Terminal**
2. Black/gray box appears at bottom

✅ **Expected:**
```
C:\Users\YourName\Desktop\fastapi>
```

---

## STEP 4: Switch to Command Prompt

PowerShell has issues. Use Command Prompt instead.

1. **Click dropdown arrow** next to `+` in terminal
2. **Select "Command Prompt"**
3. **Close PowerShell tab** (X button)

✅ **Expected:**
```
C:\Users\...\fastapi>
```

---

## STEP 5: Create Virtual Environment

**Type:**
```bash
python -m venv fastapi
```

**Wait 30 seconds** (nothing shows - normal!)

✅ **Expected:** Prompt returns

---

## STEP 6: Activate Virtual Environment

**Type:**
```bash
fastapi\Scripts\activate
```

✅ **Expected:**
```
(fastapi) C:\Users\...\fastapi>
```

Notice `(fastapi)` at start = activated! ✨

---

## STEP 7: Install FastAPI & Uvicorn

**Type:**
```bash
pip install fastapi uvicorn
```

**Wait 1-2 minutes**

✅ **Expected:**
```
Successfully installed fastapi-0.x.x uvicorn-0.x.x ...
```

---

---

# PHASE 2: CREATE PROJECT FILES

## STEP 8: Create `models.py`

**What:** Blueprint for Products

**In Explorer:**
1. Right-click empty space
2. **New File**
3. Type: `models.py`
4. Press Enter

**Copy and Paste this code:**

```python
from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    desc: str
    price: int
    quantity: int
```

**Explanation:**
- `id: int` = Product ID (unique number)
- `name: str` = Product name (text)
- `desc: str` = Description (text)
- `price: int` = Price in rupees (number)
- `quantity: int` = Stock quantity (number)

**Save:** `Ctrl + S`

✅ **Expected:** No red errors

---

## STEP 9: Create `main.py` (THE MAIN FILE!)

**What:** All your API endpoints (routes)

**In Explorer:**
1. Right-click empty space
2. **New File**
3. Type: `main.py`
4. Press Enter

**Copy and Paste ENTIRE code below:**

```python
from fastapi import FastAPI
from models import Product

app = FastAPI()

# ========================================
# IN-MEMORY DATABASE (LIST)
# Data stored in RAM - resets when server stops
# ========================================

products_db = [
    Product(id=1, name="Notebook A4", desc="100 pages ruled notebook", price=150, quantity=50),
    Product(id=2, name="Pen Set", desc="Pack of 10 quality pens", price=300, quantity=30),
    Product(id=3, name="Pencil Set", desc="12 HB pencils", price=120, quantity=40),
    Product(id=4, name="Highlighters", desc="5 neon color highlighters", price=250, quantity=25),
    Product(id=5, name="Eraser", desc="Rubber erasers (pack of 5)", price=80, quantity=100),
]

# ========================================
# ROOT ENDPOINT
# ========================================

@app.get("/")
def home():
    """
    GET / endpoint
    Returns welcome message
    """
    return {
        "message": "Welcome to Stationary Store API!",
        "total_products": len(products_db)
    }

# ========================================
# CREATE - Add new product
# ========================================

@app.post("/products/")
def create_product(product: Product):
    """
    POST /products/ endpoint
    Add new product to database
    Input: Product object (id, name, desc, price, quantity)
    Output: Confirmation message
    """
    # Check if product with this ID already exists
    for p in products_db:
        if p.id == product.id:
            return {"error": f"Product with id={product.id} already exists"}
    
    # Add new product
    products_db.append(product)
    return {
        "message": "Product created successfully",
        "product": product,
        "total_products": len(products_db)
    }

# ========================================
# READ - Get all products
# ========================================

@app.get("/products/")
def get_all_products():
    """
    GET /products/ endpoint
    Returns all products from database
    """
    return {
        "total": len(products_db),
        "products": products_db
    }

# ========================================
# READ - Get one product by ID
# ========================================

@app.get("/products/{product_id}")
def get_product(product_id: int):
    """
    GET /products/{product_id} endpoint
    Returns single product by ID
    Example: /products/1 → returns product with id=1
    """
    for product in products_db:
        if product.id == product_id:
            return {
                "found": True,
                "product": product
            }
    
    return {
        "found": False,
        "error": f"Product with id={product_id} not found"
    }

# ========================================
# UPDATE - Modify existing product
# ========================================

@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):
    """
    PUT /products/{product_id} endpoint
    Update existing product (replace all fields)
    """
    for i in range(len(products_db)):
        if products_db[i].id == product_id:
            products_db[i] = product
            return {
                "message": "Product updated successfully",
                "product": product
            }
    
    return {
        "error": f"Product with id={product_id} not found"
    }

# ========================================
# DELETE - Remove product
# ========================================

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    """
    DELETE /products/{product_id} endpoint
    Remove product from database
    """
    global products_db
    initial_count = len(products_db)
    products_db = [p for p in products_db if p.id != product_id]
    
    if len(products_db) < initial_count:
        return {
            "message": f"Product with id={product_id} deleted successfully",
            "remaining_products": len(products_db)
        }
    else:
        return {
            "error": f"Product with id={product_id} not found"
        }

# ========================================
# BONUS - Filter by price range
# ========================================

@app.get("/products/price-range/{min_price}/{max_price}")
def get_products_by_price(min_price: int, max_price: int):
    """
    GET /products/price-range/{min_price}/{max_price} endpoint
    Find products within price range
    Example: /products/price-range/100/200 → products between 100-200 rupees
    """
    filtered = [p for p in products_db if min_price <= p.price <= max_price]
    return {
        "price_range": f"{min_price}-{max_price}",
        "count": len(filtered),
        "products": filtered
    }

# ========================================
# BONUS - Find low stock products
# ========================================

@app.get("/products/low-stock/{threshold}")
def get_low_stock(threshold: int):
    """
    GET /products/low-stock/{threshold} endpoint
    Find products with quantity below threshold
    Example: /products/low-stock/30 → products with less than 30 in stock
    """
    low_stock = [p for p in products_db if p.quantity < threshold]
    return {
        "threshold": threshold,
        "count": len(low_stock),
        "products": low_stock
    }
```

**Key Points:**
- **In-memory database** = `products_db = [...]` (list in RAM)
- **5 Stationary Products** pre-loaded:
  1. Notebook A4 - 150 rupees - 50 qty
  2. Pen Set - 300 rupees - 30 qty
  3. Pencil Set - 120 rupees - 40 qty
  4. Highlighters - 250 rupees - 25 qty
  5. Eraser - 80 rupees - 100 qty
- **8 Endpoints** (routes): GET, POST, PUT, DELETE + 2 bonus filters

**Save:** `Ctrl + S`

✅ **Expected:** No red errors

---

---

# PHASE 3: RUN YOUR API

## STEP 10: Start the Server

**In terminal** (with `(fastapi)` showing)

**Type:**
```bash
uvicorn main:app --reload
```

**Wait 3-5 seconds**

✅ **Expected:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

Keep terminal open - server runs here!

---

## STEP 11: Open Documentation

**Open your browser**

**Visit:**
```
http://127.0.0.1:8000/docs
```

✅ **Expected:**
- Swagger UI page loads
- All 8 endpoints visible:
  - GET /
  - POST /products/
  - GET /products/
  - GET /products/{product_id}
  - PUT /products/{product_id}
  - DELETE /products/{product_id}
  - GET /products/price-range/{min_price}/{max_price}
  - GET /products/low-stock/{threshold}

---

---

# PHASE 4: TEST EVERYTHING

## TEST 1: Get Root Message (GET /)

1. **Click** endpoint `GET /`
2. **Click** "Try it out"
3. **Click** "Execute"

✅ **Response:**
```json
{
  "message": "Welcome to Stationary Store API!",
  "total_products": 5
}
```

---

## TEST 2: Get All Products (GET /products/)

1. **Click** `GET /products/`
2. **Click** "Try it out"
3. **Click** "Execute"

✅ **Response:**
```json
{
  "total": 5,
  "products": [
    {
      "id": 1,
      "name": "Notebook A4",
      "desc": "100 pages ruled notebook",
      "price": 150,
      "quantity": 50
    },
    {
      "id": 2,
      "name": "Pen Set",
      "desc": "Pack of 10 quality pens",
      "price": 300,
      "quantity": 30
    },
    {
      "id": 3,
      "name": "Pencil Set",
      "desc": "12 HB pencils",
      "price": 120,
      "quantity": 40
    },
    {
      "id": 4,
      "name": "Highlighters",
      "desc": "5 neon color highlighters",
      "price": 250,
      "quantity": 25
    },
    {
      "id": 5,
      "name": "Eraser",
      "desc": "Rubber erasers (pack of 5)",
      "price": 80,
      "quantity": 100
    }
  ]
}
```

✅ **What this means:** All 5 stationary products loaded!

---

## TEST 3: Get One Product (GET /products/{product_id})

1. **Click** `GET /products/{product_id}`
2. **Click** "Try it out"
3. **In field** `product_id`, type: `2`
4. **Click** "Execute"

✅ **Response:**
```json
{
  "found": true,
  "product": {
    "id": 2,
    "name": "Pen Set",
    "desc": "Pack of 10 quality pens",
    "price": 300,
    "quantity": 30
  }
}
```

✅ **What this means:** Found Pen Set (id=2)!

---

## TEST 4: Create New Product (POST /products/)

1. **Click** `POST /products/`
2. **Click** "Try it out"
3. **In Request body**, paste:

```json
{
  "id": 6,
  "name": "Calculator",
  "desc": "Scientific calculator with 240 functions",
  "price": 499,
  "quantity": 15
}
```

4. **Click** "Execute"

✅ **Response:**
```json
{
  "message": "Product created successfully",
  "product": {
    "id": 6,
    "name": "Calculator",
    "desc": "Scientific calculator with 240 functions",
    "price": 499,
    "quantity": 15
  },
  "total_products": 6
}
```

✅ **What this means:** New product added! Now 6 total.

---

## TEST 5: Verify New Product Was Added

1. **Click** `GET /products/`
2. **Click** "Try it out"
3. **Click** "Execute"

✅ **Response includes all 6 products** (original 5 + Calculator)

---

## TEST 6: Update a Product (PUT /products/{product_id})

Let's update product #1 (Notebook A4)

1. **Click** `PUT /products/{product_id}`
2. **Click** "Try it out"
3. **In field** `product_id`, type: `1`
4. **In Request body**, paste:

```json
{
  "id": 1,
  "name": "Notebook A4 Premium",
  "desc": "200 pages premium ruled notebook",
  "price": 200,
  "quantity": 45
}
```

5. **Click** "Execute"

✅ **Response:**
```json
{
  "message": "Product updated successfully",
  "product": {
    "id": 1,
    "name": "Notebook A4 Premium",
    "desc": "200 pages premium ruled notebook",
    "price": 200,
    "quantity": 45
  }
}
```

✅ **What this means:** Notebook updated with new name, price, and quantity!

---

## TEST 7: Delete a Product (DELETE /products/{product_id})

Let's delete product #3 (Pencil Set)

1. **Click** `DELETE /products/{product_id}`
2. **Click** "Try it out"
3. **In field** `product_id`, type: `3`
4. **Click** "Execute"

✅ **Response:**
```json
{
  "message": "Product with id=3 deleted successfully",
  "remaining_products": 5
}
```

✅ **What this means:** Pencil Set deleted! Only 5 products left.

---

## TEST 8: Verify Deletion

1. **Click** `GET /products/`
2. **Click** "Try it out"
3. **Click** "Execute"

✅ **Response:** Only 5 products (Pencil Set is gone!)

---

## TEST 9: Try to Get Deleted Product

1. **Click** `GET /products/{product_id}`
2. **Click** "Try it out"
3. **In field** `product_id`, type: `3`
4. **Click** "Execute"

✅ **Response:**
```json
{
  "found": false,
  "error": "Product with id=3 not found"
}
```

✅ **What this means:** Confirms deletion worked!

---

## TEST 10: Filter by Price Range (GET /products/price-range/{min_price}/{max_price})

Find products between 100-200 rupees

1. **Click** `GET /products/price-range/{min_price}/{max_price}`
2. **Click** "Try it out"
3. **In field** `min_price`, type: `100`
4. **In field** `max_price`, type: `200`
5. **Click** "Execute"

✅ **Response:** Products in 100-200 range

```json
{
  "price_range": "100-200",
  "count": 2,
  "products": [
    {
      "id": 1,
      "name": "Notebook A4 Premium",
      "price": 200,
      "quantity": 45
    },
    {
      "id": 3,
      "name": "Pencil Set",
      "price": 120,
      "quantity": 40
    }
  ]
}
```

---

## TEST 11: Find Low Stock Products (GET /products/low-stock/{threshold})

Find products with less than 30 in stock

1. **Click** `GET /products/low-stock/{threshold}`
2. **Click** "Try it out"
3. **In field** `threshold`, type: `30`
4. **Click** "Execute"

✅ **Response:** Products with quantity < 30

```json
{
  "threshold": 30,
  "count": 2,
  "products": [
    {
      "id": 4,
      "name": "Highlighters",
      "quantity": 25
    },
    {
      "id": 5,
      "name": "Eraser",
      "quantity": 100
    }
  ]
}
```

---

---

# STOPPING AND RESTARTING

## How to Stop

**In terminal with server running:**

Press `Ctrl + C`

✅ **Result:** Server stops

---

## How to Restart Next Time

**Every time you work on project:**

```bash
fastapi\Scripts\activate
```

Then:

```bash
uvicorn main:app --reload
```

Then visit: `http://127.0.0.1:8000/docs`

---

---

# YOUR PROJECT STRUCTURE

After completing:

```
fastapi/
├── models.py              ← Product blueprint
├── main.py               ← API with 8 endpoints
├── fastapi/              ← Virtual environment
│   ├── Scripts/
│   ├── Lib/
│   └── ...
├── pyvenv.cfg
└── .gitignore
```

---

# IN-MEMORY DATABASE EXPLANATION

**What you're using:**
```python
products_db = [
    Product(id=1, name="Notebook A4", ...),
    Product(id=2, name="Pen Set", ...),
    # ... more products
]
```

**Advantages:**
- ✅ Super fast (data in RAM)
- ✅ Simple to understand
- ✅ Perfect for learning

**Disadvantages:**
- ❌ Data lost when server stops
- ❌ Not for production
- ❌ Only works on one server

**Future:** Replace with SQLite or PostgreSQL for permanent storage

---

# WHAT YOU'VE LEARNED

| Concept | What It Is |
|---------|-----------|
| **Virtual Environment** | Isolated Python space |
| **FastAPI** | Web framework for APIs |
| **Uvicorn** | Server that runs your API |
| **Pydantic Models** | Data blueprints (Product class) |
| **Routes/Endpoints** | URLs that do different things |
| **@app.get()** | GET endpoint (retrieve data) |
| **@app.post()** | POST endpoint (add data) |
| **@app.put()** | PUT endpoint (update data) |
| **@app.delete()** | DELETE endpoint (remove data) |
| **CRUD** | Create, Read, Update, Delete |
| **In-Memory DB** | Data storage in RAM |
| **Swagger UI** | Interactive API documentation |

---

# TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| `Scripts\activate` not found | Run `python -m venv fastapi` first |
| `ModuleNotFoundError: fastapi` | Make sure venv activated (shows `(fastapi)`), then `pip install fastapi uvicorn` |
| `The system cannot find the path` | Use Command Prompt, not PowerShell |
| Can't import models | Make sure `models.py` in same folder as `main.py` |
| Port 8000 already in use | Run: `uvicorn main:app --port 8001 --reload` |
| Swagger UI blank | Refresh browser (Ctrl+R). Check terminal for errors. |
| Changes not showing | Save Python file (Ctrl+S). Server auto-restarts with `--reload`. |
| Tried to create product with same ID | Error message appears: "Product with id=X already exists" |

---

# CHECKLIST - Complete All

### Environment Setup
- [ ] Python installed
- [ ] VS Code installed
- [ ] `fastapi` folder on Desktop
- [ ] Virtual environment created
- [ ] Virtual environment activated (shows `(fastapi)`)
- [ ] FastAPI + Uvicorn installed

### Files Created
- [ ] `models.py` created (Product class)
- [ ] `main.py` created (all endpoints)
- [ ] Both files saved

### Server Running
- [ ] Terminal shows `Uvicorn running on http://127.0.0.1:8000`
- [ ] Browser shows Swagger UI at `http://127.0.0.1:8000/docs`

### Tests Passing
- [ ] TEST 1: GET / works
- [ ] TEST 2: GET /products/ shows 5 products
- [ ] TEST 3: GET /products/2 returns Pen Set
- [ ] TEST 4: POST /products/ creates Calculator
- [ ] TEST 5: Verify new product in list (6 total)
- [ ] TEST 6: PUT /products/1 updates Notebook
- [ ] TEST 7: DELETE /products/3 deletes Pencil Set
- [ ] TEST 8: Verify product deleted
- [ ] TEST 9: GET deleted product returns error
- [ ] TEST 10: Price range filter works
- [ ] TEST 11: Low stock filter works

### Ready for Next Phase
- [ ] All tests passing
- [ ] Server stops/starts correctly
- [ ] Understanding CRUD operations
- [ ] Code backup made

---

# STATIONARY PRODUCTS IN YOUR API

| ID | Product | Price | Stock |
|----|---------|-------|-------|
| 1 | Notebook A4 | ₹150 | 50 |
| 2 | Pen Set | ₹300 | 30 |
| 3 | Pencil Set | ₹120 | 40 |
| 4 | Highlighters | ₹250 | 25 |
| 5 | Eraser | ₹80 | 100 |

---

# NEXT PHASES (When Ready)

1. **Add Real Database** → SQLite, PostgreSQL, MongoDB
2. **Add Validation** → Check prices, quantities
3. **Add Authentication** → User login system
4. **Add Categories** → Group products by type
5. **Deploy to Cloud** → Make public (Heroku, Railway)

