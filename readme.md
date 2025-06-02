# 🏧 ATM & Customer Management System

A comprehensive Python application featuring ATM denomination calculations and a REST API for customer management with parallel processing capabilities.

## 📋 Table of Contents

- [🏧 ATM \& Customer Management System](#-atm--customer-management-system)
  - [📋 Table of Contents](#-table-of-contents)
  - [🚀 Quick Start](#-quick-start)
  - [🔧 Usage](#-usage)
    - [ATM Denomination Calculator](#atm-denomination-calculator)
    - [Customer Simulator](#customer-simulator)
  - [📚 API Documentation](#-api-documentation)
    - [Base URL Configuration](#base-url-configuration)
    - [Endpoints](#endpoints)
      - [📝 POST /customers](#-post-customers)
      - [📋 GET /customers](#-get-customers)
      - [🗑️ DELETE /customers](#️-delete-customers)
    - [Architecture](#architecture)
    - [Dependencies](#dependencies)
  - [🔧 Technical Notes](#-technical-notes)

## 🚀 Quick Start

1. **Clone and Setup**
   ```bash
   git clone https://github.com/jpcoder111/backend-project.git
   cd backend-project
   ```

2. **Create Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   # Create .env file with deployed API
   echo "BASE_URL=https://backend-project-five-blush.vercel.app/" > .env
   ```

   **For local development:**
   ```bash
   # Configure environment variables
   echo "BASE_URL=http://localhost:8000" > .env
   echo "REDIS_HOST=your-redis-host" >> .env
   echo "REDIS_PORT=6379" >> .env  
   echo "REDIS_PASSWORD=your-redis-password" >> .env

   # Start local API server
   uvicorn app.main:app --host 0.0.0.0 --reload
   ```

5. **Run Scripts**
   ```bash
   # ATM Calculator
   python -m src.scripts.denomination_routine
   
   # Customer Simulator
   python -m src.scripts.customer_simulation
   ```

## 🔧 Usage

### ATM Denomination Calculator

Calculates all possible payout combinations for specified amounts using available denominations.
The solution is obtained efficiently utilizing a "backtracking" algorithm.

```bash
python -m src.scripts.denomination_routine
```

**Example Output:**
```
30 EUR:
- 3 x 10 EUR

50 EUR:
- 5 x 10 EUR
- 1 x 50 EUR
```

**Output Location:** `outputs/denomination_routine_run.txt`

### Customer Simulator

Sends parallel requests to test the API with randomly generated customer data.

```bash
# Customer Simulator (with optional parameters)
python -m src.scripts.customer_simulation [num_post_requests] [num_get_requests]

# Examples:
python -m src.scripts.customer_simulation          # Default: 3 POST, 3 GET
python -m src.scripts.customer_simulation 5        # 5 POST, 3 GET (default)
python -m src.scripts.customer_simulation 5 2      # 5 POST, 2 GET
```

**Output Location:** `outputs/customer_simulation_YYYYMMDD_HHMMSS.log`


## 📚 API Documentation

### Base URL Configuration

Create a `.env` file in the project root:

```env
# Production (Deployed)
BASE_URL=https://backend-project-five-blush.vercel.app/

# Development (Local)
BASE_URL=http://localhost:8000
```

### Endpoints

#### 📝 POST /customers
Inserts new customers to the list.

**Request Body:**
```json
[
    {
        "firstName": "John",
        "lastName": "Doe",
        "age": 25,
        "id": 1
    }
]
```

**Response:** Inserted and failed customers

#### 📋 GET /customers
Retrieves all customers sorted by last name, then first name.

**Response:**
```json
[
    {
        "firstName": "John",
        "lastName": "Doe",
        "age": 25,
        "id": 1
    }
]
```

#### 🗑️ DELETE /customers
Removes all customers (testing/evaluation endpoint).

**Response:**
204 No Content


### Architecture

```
├── main.py # FastAPI application with endpoints
├── outputs/ # Generated output files and logs
├── src/
  ├── scripts/ # Executable scripts
  ├── services/ # Business logic
  ├── clients/ # Database/storage connection utilities
  └── types/ # Data models and types
```

### Dependencies

- **FastAPI**: Modern web framework for building APIs
- **Pydantic**: Data validation and settings management
- **aiohttp**: Async HTTP client for parallel requests
- **python-dotenv**: Environment variable management

## 🔧 Technical Notes

1. **Customer Uniqueness**: Each POST request from the simulator ensures no duplicate customers are sent, where uniqueness is determined by the combination of firstName and lastName.

2. **Data Persistence Strategy**: The system utilizes Redis as a persistent database with a collection-based storage pattern. Customer insertion follows a read-modify-write approach: retrieve existing customers, determine the correct insertion position through lexicographic comparison of names, insert the new record, and persist the updated collection.

3. **Deployment**: The app was deployed into Vercel. Running the app locally should connect to the same database that the deployed application.

4. **Concurrency Implementation**: The customer simulator leverages Python's `asyncio` library and `aiohttp` for high-performance parallel request processing. Multiple POST and GET requests are created as asynchronous tasks, then executed concurrently using `asyncio.gather()`. This approach allows the simulator to send numerous API requests simultaneously rather than sequentially, significantly improving performance and providing realistic load testing scenarios. The tasks are randomly shuffled before execution to simulate real-world traffic patterns.