import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.core.database import SessionLocal
from app.models.household import Household
from app.services.ml_service import ml_service


def test_ml_service_models_loaded():
    assert ml_service.is_ready() is True
    assert ml_service.clf is not None
    assert ml_service.kmeans is not None
    assert ml_service.regressor is not None
    assert ml_service.scaler is not None

    metrics = ml_service.get_system_metrics()
    assert "clustering" in metrics
    assert "classifier" in metrics
    assert "demand_forecaster" in metrics
    assert metrics["clustering"]["n_clusters"] == 4
    assert metrics["classifier"]["algorithm"] == "Random Forest Classifier"


def test_ml_service_prediction_flow():
    db = SessionLocal()
    try:
        household = db.query(Household).first()
        assert household is not None

        prediction = ml_service.predict(household)
        assert prediction["status"] == "AVAILABLE"
        assert prediction["predicted_tier"] in ("CRITICAL", "HIGH", "MEDIUM", "LOW")
        assert 0 <= prediction["confidence_pct"] <= 100
        assert "cluster" in prediction
        assert "title_ar" in prediction["cluster"]
        assert "demand_forecast" in prediction
        assert prediction["demand_forecast"]["estimated_aid_amount_yer"] > 0
        assert len(prediction["top_contributing_factors"]) > 0
    finally:
        db.close()


def test_ml_api_dual_perspective():
    client = TestClient(app)
    
    # 1. Login as officer
    login_res = client.post(
        "/api/v1/auth/login",
        json={"username": "programs_officer", "password": "Officer@2026"},
    )
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Check ML models summary endpoint
    summary_res = client.get("/api/v1/needs/metrics/ml-summary", headers=headers)
    assert summary_res.status_code == 200
    summary_data = summary_res.json()
    assert summary_data["classifier"]["algorithm"] == "Random Forest Classifier"

    # 3. Check Household Needs Assessment with ML dual perspective
    db = SessionLocal()
    try:
        h = db.query(Household).first()
        assert h is not None
        h_id = str(h.id)
    finally:
        db.close()

    needs_res = client.get(f"/api/v1/needs/{h_id}", headers=headers)
    assert needs_res.status_code == 200
    data = needs_res.json()
    assert "calculated_score" in data
    assert "ml_insights" in data
    assert data["ml_insights"]["status"] == "AVAILABLE"
    assert "cluster" in data["ml_insights"]
    assert "predicted_tier" in data["ml_insights"]
