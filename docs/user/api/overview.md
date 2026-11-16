# 🔌 API Reference — sc-oam-app

Auto-generated FastAPI documentation is available at `http://127.0.0.1:8000/docs` when the server is running. This section provides a structured, human-readable reference for API consumers.

---

## 🌐 Base URL

| Environment | Base URL |
|-------------|----------|
| **Development** | `http://127.0.0.1:8000/api` |
| **Production** | `https://your-domain.com/api` |

All endpoints prefix with `/api`. The default development host is `127.0.0.1:8000`.

---

## 🏓 Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| **GET** | `/api/health` | Simple health check — returns JSON status |

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
| **GET** | `/api/blueprints/` | List all blueprints — supports `?category=&?ilg_label=` filter params |
| **POST** | `/api/blueprints/` | Create a new blueprint entry |
| **GET** | `/api/blueprints/{id}` | Get a specific blueprint by database ID |
| **PUT** | `/api/blueprints/{id}` | Partially update a blueprint (fields are optional) |
| **DELETE** | `/api/blueprints/{id}` | Delete a blueprint — returns `204 No Content` |

### List Blueprints

```bash
curl http://127.0.0.1:8000/api/blueprints/
```

### Create Blueprint

```bash
curl -X POST http://127.0.0.1:8000/api/blueprints/ \
  -H "Content-Type: application/json" \
  -d '{"blueprint_id":"bp_001","bp_name":"My Blueprint","category":"weapons","subcategory":"missiles","craft_type":"missile","output_item_name":"missile","quality_min":500.0,"quality_max":800.0,"craft_time_seconds":30.0,"ilg_label":"Weapons/Missiles"}'
```

### Get Blueprint

```bash
curl http://127.0.0.1:8000/api/blueprints/1
```

### Update Blueprint

```bash
curl -X PUT http://127.0.0.1:8000/api/blueprints/1 \
  -H "Content-Type: application/json" \
  -d '{"quality_min":600.0}'
```

### Delete Blueprint

```bash
curl -X DELETE http://127.0.0.1:8000/api/blueprints/1
```

---

## 🔧 Crafting

| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST** | `/api/crafting/quality` | Calculate quality score for given resources |
| **POST** | `/api/crafting/result` | Get crafting result with tier determination |

### Calculate Quality

```bash
curl -X POST http://127.0.0.1:8000/api/crafting/quality \
  -H "Content-Type: application/json" \
  -d '{"blueprint_id":1,"type":"missile","amount":1.0,"count":1,"quality_selector":750.0}'
```

### Get Crafting Result

```bash
curl -X POST http://127.0.0.1:8000/api/crafting/result \
  -H "Content-Type: application/json" \
  -d '{"blueprint_id":1,"type":"missile","amount":1.0,"count":1,"quality_selector":750.0}'
```

---
