# API Reference

Auto-generated FastAPI documentation is available at `http://127.0.0.1:8000/docs` when the server is running.
This section provides a structured overview of all endpoints.

## 📊 Base URL

All API endpoints prefix with `/api`

| Environment | Base URL |
|-------------|----------|
| **Development** | `http://127.0.0.1:8000/api` |
| **Production** | `https://your-domain.com/api` |

## 🏓 Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| **GET** | `/api/health` | Simple health check |

### Example

```bash
curl http://127.0.0.1:8000/api/health
```

### Response

```json
{
  "status": "ok",
  "service": "OAM API",
  "version": "0.1.0"
}
```

---

## 📋 Blueprints

| Method | Endpoint | Description |
|--------|----------|-------------|
| **GET** | `/api/blueprints/` | List all blueprints |
| **POST** | `/api/blueprints/` | Create new blueprint |
| **GET** | `/api/blueprints/{id}` | Get blueprint by ID |
| **PUT** | `/api/blueprints/{id}` | Update blueprint |
| **DELETE** | `/api/blueprints/{id}` | Delete blueprint |

### List Blueprints

```bash
curl http://127.0.0.1:8000/api/blueprints/
```

### Create Blueprint

```bash
curl -X POST http://127.0.0.1:8000/api/blueprints/ \
  -H "Content-Type: application/json" \
  -d '{"blueprint_id": "bp_001", "bp_name": "My Blueprint", "category": "weapons", "subcategory": "missiles", "craft_type": "missile", "output_item_name": "missile", "quality_min": 500.0, "quality_max": 800.0, "craft_time_seconds": 30.0, "ilg_label": "Weapons/Missiles"}'
```

### Get Blueprint

```bash
curl http://127.0.0.1:8000/api/blueprints/1
```

### Update Blueprint

```bash
curl -X PUT http://127.0.0.1:8000/api/blueprints/1 \
  -H "Content-Type: application/json" \
  -d '{"quality_min": 600.0}'
```

### Delete Blueprint

```bash
curl -X DELETE http://127.0.0.1:8000/api/blueprints/1
```

---

## 🔧 Crafting

| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST** | `/api/crafting/quality` | Calculate quality score |
| **POST** | `/api/crafting/result` | Get crafting result |

### Calculate Quality

```bash
curl -X POST http://127.0.0.1:8000/api/crafting/quality \
  -H "Content-Type: application/json" \
  -d '{"blueprint_id": 1, "type": "missile", "amount": 1.0, "count": 1, "quality_selector": 750.0}'
```

### Get Crafting Result

```bash
curl -X POST http://127.0.0.1:8000/api/crafting/result \
  -H "Content-Type: application/json" \
  -d '{"blueprint_id": 1, "type": "missile", "amount": 1.0, "count": 1, "quality_selector": 750.0}'
```

---

## 📦 Warehouse

| Method | Endpoint | Description |
|--------|----------|-------------|
| **GET** | `/api/warehouse/` | List warehouse inventory |

### Example

```bash
curl http://127.0.0.1:8000/api/warehouse/
```

---

## ⚓ Hangar

| Method | Endpoint | Description |
|--------|----------|-------------|
| **GET** | `/api/hangar/` | List fleet vessels |

### Example

```bash
curl http://127.0.0.1:8000/api/hangar/
```

---

## 📊 Data Models

| Model | Endpoint | Description |
|-------|----------|-------------|
| **BlueprintBase** | N/A | Base fields for blueprint |
| **BlueprintCreate** | `/api/blueprints/` | Fields for creating |
| **BlueprintUpdate** | `/api/blueprints/{id}` | Fields for updating |
| **BlueprintResponse** | All blueprint endpoints | Full blueprint with ID |
| **QualityCalculation** | `/api/crafting/quality` | Quality calculation result |
| **ResourceRequirement** | `/api/crafting/*` | Crafting resource params |
| **CraftingResult** | `/api/crafting/result` | Crafting operation result |

---

## 🔐 Authentication (Planned)

| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST** | `/api/auth/login` | JWT token generation |
| **POST** | `/api/auth/refresh` | Refresh access token |
| **POST** | `/api/auth/logout` | Invalidate token |

*Authentication is planned for future releases. Currently, endpoints are open for development purposes.*

---

## 📚 OpenAPI/Swagger

When the server is running, visit:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

Both provide interactive API exploration, parameter validation, and example requests/responses.
