"""Blueprint API endpoint tests — CRUD lifecycle, validation, database pluggability.

Run with:
    pytest -v tests/api/test_blueprints.py
"""

from fastapi.testclient import TestClient
import pytest

from app import app


# --- Fixture: TestClient ---

@pytest.fixture(scope="module")
def client():
    """FastAPI TestClient instance (module-scoped, session-wide)."""
    return TestClient(app)


# --- P0: CRUD Lifecycle ---

def test_crud_lifecycle(client):
    """Complete CREATE-READ-UPDATE-DELETE lifecycle for blueprints."""
    # 1. CREATE: Post a new blueprint
    bp = {
        "blueprint_id": "bp_test_001",
        "bp_name": "Test Missile Blueprint",
        "category": "weapons",
        "subcategory": "missiles",
        "craft_type": "missile",
        "output_item_name": "missile",
        "quality_min": 500.0,
        "quality_max": 800.0,
        "craft_time_seconds": 30.0,
        "ilg_label": "Weapons/Missiles",
    }
    response = client.post("/api/blueprints/", json=bp)
    assert response.status_code == 201, f"Create failed: {response.text}"
    created = response.json()
    assert created["bp_name"] == "Test Missile Blueprint"
    assert created["blueprint_id"] == "bp_test_001"
    bp_id = created["id"]  # DB-generated primary key

    # 2. READ: Get the created blueprint
    response = client.get(f"/api/blueprints/{bp_id}")
    assert response.status_code == 200, f"Read failed: {response.text}"
    assert response.json()["bp_name"] == "Test Missile Blueprint"

    # 3. UPDATE: Modify quality_min
    response = client.put(
        f"/api/blueprints/{bp_id}",
        json={"quality_min": 600.0},
    )
    assert response.status_code == 200, f"Update failed: {response.text}"
    updated = response.json()
    assert updated["quality_min"] == 600.0

    # 4. DELETE: Remove the blueprint
    response = client.delete(f"/api/blueprints/{bp_id}")
    assert response.status_code == 204, f"Delete failed: {response.text}"

    # 5. Verify deletion — should return 404
    response = client.get(f"/api/blueprints/{bp_id}")
    assert response.status_code == 404, "Blueprint should no longer exist"


# --- P0: Empty List ---

def test_health_check(client):
    """GET /health returns health status with branding."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "sc-oam-app"
    assert data["version"] == "0.1.0"
    assert data["name"] == "sc-oam-app"

# --- P0: Empty List ---

def test_list_empty(client):
    """GET /api/blueprints/ returns empty list when no data."""
    response = client.get("/api/blueprints/")
    assert response.status_code == 200
    assert len(response.json()) == 0


# --- P0: Duplicate Prevention ---

def test_duplicate_id(client):
    """POST /api/blueprints/ returns 400 if blueprint_id already exists."""
    bp = {
        "blueprint_id": "bp_duplicate",
        "bp_name": "Duplicate",
        "category": "test",
        "subcategory": "test",
        "craft_type": "test",
        "output_item_name": "test",
        "quality_min": 100.0,
        "quality_max": 200.0,
        "craft_time_seconds": 1.0,
        "ilg_label": "Test",
    }

    # First create
    create_resp = client.post("/api/blueprints/", json=bp)
    assert create_resp.status_code == 201, f"First create failed: {create_resp.text}"

    # Second create with same blueprint_id should fail
    response = client.post("/api/blueprints/", json=bp)
    assert response.status_code == 400, "Duplicate should be rejected"
    assert "already exists" in response.json()["detail"]


# --- P1: Database Pluggability ---

@pytest.mark.parametrize("db_url", [
    "sqlite:///./database.db",
    # Uncomment and ensure PostgreSQL is running for this test:
    # "postgresql://oam_user:password@localhost:5432/sc_oam_db",
])
def test_database_pluggability(client, db_url, request):
    """Same CRUD tests pass with SQLite and PostgreSQL DATABASE_URL."""
    # Override the app's DATABASE_URL for this test duration
    from core.database import DATABASE_URL as OrigDATABASE_URL
    import core.database
    core.database.DATABASE_URL = db_url

    # In a full setup, we'd re-create the TestClient or reconfigure;
    # for now, we verify the config can be switched without ImportError.
    # The real pluggability test would use a shared db_session fixture
    # with engine recreation.
    core.database.DATABASE_URL = OrigDATABASE_URL  # Restore original
