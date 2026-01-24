# 🚀 FastAPI Project Structure Generators

This repository provides **automated Python scripts** to generate production-ready FastAPI project structures with two different architectural patterns:

1. **Layer-Based Architecture** (Traditional MVC-style)
2. **Feature-Based Architecture** (Domain-driven approach)

## 📜 Available Scripts

### 1️⃣ Layer-Based Structure Generator
**File:** `create_fastapi_layer_structure.py`

Generates a project with **horizontal layers** where code is organized by technical concerns:
```
src/
├── routers/           # API endpoints (Presentation Layer)
├── schemas/           # Pydantic models (DTOs)
├── models/            # Database models (Data Layer)
├── services/          # Business logic (Service Layer)
├── repositories/      # Data access (Repository Layer)
├── dependencies/      # Shared dependencies
├── core/              # Configuration, security, logging
├── db/                # Database setup
└── api/               # API versioning
```

**Usage:**
```sh
python create_fastapi_layer_structure.py my_project --output .
```

### 2️⃣ Feature-Based Structure Generator
**File:** `create_fastapi_feature_structure.py`

Generates a project with **vertical features** where each feature is self-contained:
```
src/
├── features/          # Self-contained features
│   ├── auth/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── services.py
│   │   ├── routes.py
│   │   └── dependencies.py
│   └── users/
│       └── ... (same structure)
└── shared/            # Cross-cutting concerns
    ├── config/
    ├── database/
    ├── security/
    └── utils/
```

**Usage:**
```sh
python create_fastapi_feature_structure.py my_project --output .
```

## 🎯 Which Architecture Should You Choose?

### Layer-Based Architecture ✅
- **Best for:** Small to medium projects, teams familiar with traditional MVC/3-tier architecture
- **Pros:** 
  - Clear separation of concerns by technical responsibility
  - Easy to locate all routers, services, or models in one place
  - Familiar to developers with traditional backend experience
  - Repository pattern for cleaner data access
- **Cons:** 
  - Features are spread across multiple directories
  - Can become harder to maintain as the project grows
  - Risk of tight coupling between layers

### Feature-Based Architecture ✅
- **Best for:** Large projects, microservices-ready applications, domain-driven design
- **Pros:** 
  - High cohesion - each feature is self-contained
  - Easy to scale and add new features independently
  - Feature isolation makes testing easier
  - Better for team collaboration (teams can own features)
  - Easier to extract features into microservices later
- **Cons:** 
  - Slightly more complex initial setup
  - May have some code duplication across features
  - Requires discipline to maintain shared utilities properly

## 🚀 Getting Started

### **1. Clone the Repository**
```sh
git clone https://github.com/Keirishan/FastAPI-Project-Folder-Structure-Creator.git
cd FastAPI-Project-Folder-Structure-Creator
```

### **2. Choose Your Architecture**
Run either script based on your preference:

**For Layer-Based:**
```sh
python create_fastapi_layer_structure.py my_awesome_api
```

**For Feature-Based:**
```sh
python create_fastapi_feature_structure.py my_awesome_api
```

### **3. Set Up Your Generated Project**
```sh
cd my_awesome_api
pip install .
python scripts/init_db.py
uvicorn my_awesome_api.main:app --reload
```

## 📦 Generated Project Features

Both architectures include:
- ✅ **JWT Authentication** with login/logout
- ✅ **SQLAlchemy Async** with PostgreSQL
- ✅ **Alembic Migrations**
- ✅ **Pydantic Settings** with environment variables
- ✅ **Structured Logging**
- ✅ **Role-Based Access Control**
- ✅ **Production-Ready Configuration**
- ✅ **Admin User Seeding**

## 📄 License
MIT License - Feel free to use for your projects!
