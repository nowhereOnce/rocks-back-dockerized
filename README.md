# 🪨 Rock Samples API - Enterprise Dockerized Backend

A robust, asynchronous REST API built with **FastAPI** and **SQLModel**, designed for the management and cataloging of geological specimens. This system leverages **Docker** for seamless deployment and **NGINX** as a high-performance reverse proxy.

---

## 🏗️ System Architecture

The application is architected using a microservices-ready approach, fully containerized:

*   **Reverse Proxy (NGINX)**: Acts as the gateway, handling incoming traffic on port 80 and forwarding requests to the API. It ensures secure and efficient communication.
*   **Application Layer (FastAPI)**: An asynchronous Python backend that manages business logic, validation, and security.
*   **Database Layer (PostgreSQL)**: A relational database for persistent storage, accessible only via the internal Docker network for enhanced security.
*   **Worker/Initialization**: Automated data pipeline that seeds the database from CSV files upon startup.

---

## 🗄️ Database Architecture

The database is designed with **SQLModel**, ensuring strict type safety and high performance. All entities use **UUID v4** as primary keys to prevent ID enumeration and ensure global uniqueness.

### Entity Relationship Model

1.  **User**: Manages system access.
    *   `uid` (UUID): Primary Key.
    *   `username`, `email`: Unique identifiers.
    *   `hashed_password`: Securely hashed using Bcrypt.
    *   `is_active`: Account status flag.
2.  **Rocks**: Catalog of rock types.
    *   `uid` (UUID): Primary Key.
    *   `name`: The common or scientific name.
    *   `description`: Geological properties.
3.  **Locations**: Geographic origins.
    *   `uid` (UUID): Primary Key.
    *   `name`, `country`: Where the specimen was found.
4.  **Samples**: The central entity linking all data.
    *   `uid` (UUID): Primary Key.
    *   `rock_uid` / `location_uid`: Foreign keys establishing **Many-to-One** relationships.
    *   `cut`, `thin_section`: Boolean flags for physical state.
    *   `picture`: Storage path or URL for visual records.

### Automatic Timestamps
Every table includes `created_at` and `updated_at` fields, automatically managed by PostgreSQL to maintain a clear audit trail.

---

## 🔐 Authentication & Security

The system implements a professional **OAuth2 with Password Bearer** flow using **JWT (JSON Web Tokens)**.

### The Authentication Flow
1.  **Registration**: A new user signs up via `/api/auth/signup`. Passwords are encrypted before storage.
2.  **Token Exchange**: Users send credentials to `/api/auth/token`. If valid, the server issues a JWT.
3.  **Session Management**: The JWT contains a payload with the username and an expiration timestamp (default: 15 minutes).
4.  **Authorized Requests**: For protected endpoints, the client must include the token in the header: `Authorization: Bearer <your_token>`.
5.  **Server Validation**: The backend decodes the JWT using a `SECRET_KEY`, verifies the expiration, and checks the user's status in the database.

### Password Security
Passwords are never stored in plain text. We use the **Passlib** library with the **Bcrypt** algorithm to ensure state-of-the-art hashing and salting.

---

## 🚀 API Endpoints

### 1. Authentication (`/api/auth`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/signup` | Register a new administrator/user. | No |
| `POST` | `/token` | Exchange credentials for a JWT token. | No |
| `GET` | `/me` | Get profile details of the logged-in user. | **Yes** |

### 2. Rock Management (`/api/rocks`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | List all cataloged rock types. | No |
| `GET` | `/{uid}` | Retrieve specific rock details. | No |
| `POST` | `/` | Add a new rock type to the catalog. | **Yes** |
| `PUT` | `/{uid}` | Update rock characteristics. | **Yes** |
| `DELETE` | `/{uid}` | Remove a rock type from the system. | **Yes** |

### 3. Location Management (`/api/locations`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | List all registered collection sites. | No |
| `POST` | `/` | Register a new geographic location. | No |

### 4. Sample Catalog (`/api/samples`)
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | List all physical specimens with full metadata. | No |
| `POST` | `/` | Register a new specimen (Auto-creates Rock/Location). | **Yes** |
| `DELETE` | `/{uid}` | Remove a specimen record. | **Yes** |

> **Pro Tip**: The `POST /samples` endpoint is highly efficient. You don't need to know the UUIDs for Rocks or Locations; just provide their names, and the system will link existing ones or create new records automatically.

---

## 🛠️ Installation & Deployment

### Environment Configuration
Create a `.env` file in the `app/` directory with the following variables:
```env
POSTGRES_URL=postgresql+asyncpg://rocks_user:rocks_password@postgres:5432/rocks_db
SECRET_KEY=generate_a_strong_random_string_here
ALGORITHM=HS256
```

### Docker Deployment
1.  **Build and Start**:
    ```bash
    docker-compose up --build -d
    ```
2.  **Verify Services**:
    ```bash
    docker-compose ps
    ```
3.  **Access Documentation**:
    *   **Swagger UI**: [http://localhost/api/docs](http://localhost/api/docs)
    *   **ReDoc**: [http://localhost/api/redoc](http://localhost/api/redoc)

---

## 📊 Data Initialization

On the very first launch, the system automatically executes a seeding process:
1.  It reads geological data from `app/src/datos_rocas.csv`.
2.  It uses the **Service Layer** to validate and insert records.
3.  It ensures no duplicate rocks or locations are created during the process.

---

## 👨‍💻 Author
**Aguilar Ramos Enrique Alejandro**
*Backend Engineer & Software Architect*
