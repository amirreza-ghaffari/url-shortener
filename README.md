A simple, scalable URL shortening service built with **FastAPI** and **PostgreSQL**.

This project showcases:
- ***UUID7-based** generation* for security and performance
- Logging and observability practices
---

# Why **UUID7**? why not ID or UUID4 or just random string?
there are some solutions for creating a url shortener


###  **Random strings**
when a customer submits a long url we can just use the hash function to convert it to a short url and choose first n character from it, but it can lead to hash collision.
It has some pros and cons:
- Easy to implement
- generated short urls are also long
- it needs to check db it the shortened urls exists to avoid hash collision


###  **Auto-incrementing IDs**
when a customer submits a long url we can insert it to DB and with the generated auto-incrementing ID we can create a short url by encoding the ID to base62.
- *Easy to implement*: just use the generated ID
- *Security Issue*: Predictable IDs expose business metrics
- Users can guess total URLs created
- Competitors can scrape data sequentially


### **UUID4**
To fix the security issue, we can use UUID4:
- Non-predictable and secure
- **Performance Issue**: Random UUIDs cause database **index fragmentation**
- Random inserts cause B-tree index **page splits** and higher I/O costs
- Degraded performance at scale (millions of URLs)

###  **UUID7 (_**Our Solution**_)**
- with this approach we can benefit from using uuid and fix the performance issue of uuid4 by using time-ordered uuids and avoid security issue mentioned above
- Non-sequential and unpredictable
- Cryptographically secure randomness (last 74 bits)

- **Performance Benefits:**
  - **Time-ordered** (first 48 bits = Unix timestamp in milliseconds)
  - Sequential inserts = **minimal page splits**
  - **Better B-tree index performance**
  - Optimal for write-heavy workloads


**Implementation:**
```python
# Generate UUID7 (time-ordered)
uuid7 = EncoderService.generate_uuid7()  # e.g., 018d3c5e-8f3a-7000-9abc-def012345678

# Encode to Base62 for short, user-friendly URLs
short_code = EncoderService.uuid_to_base62(uuid7)  # e.g., "2mKx9pQrT8nL4vB6"

# Store UUID as primary key, Base62 code for URLs
ShortURL(id=uuid7, short_code=short_code, original_url=url)
```

### Base62 Encoding

We encode UUID7s to Base62 (0-9, A-Z, a-z) for compact, URL-safe short codes:
- 128-bit UUID → ~22 character Base62 string
- URL-safe and readable
- Reversible: short code → UUID for fast database lookups
- No collisions (UUID uniqueness guaranteed)

---


## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/url-shortener.git
cd url-shortener
```

### 2. Create virtual environment & install dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up environment variables

```bash
cp sample.env .env
# Edit .env with your database credentials
```

Example `.env`:
```env
ENV_SETTING=dev
PG_DSN=postgresql+asyncpg://username:password@localhost:5432/url_shortener
```

### 4. Run database migrations

```bash
alembic upgrade head
```

### 5. Run the application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## API Documentation

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

