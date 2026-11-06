def test_read_root(client):
    """اختبار نقطة النهاية الجذرية للتطبيق"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "رشاد AI" in data["system"]
    assert "/api/v1/docs" in data["docs_url"]


def test_health_check(client):
    """اختبار نقطة فحص صحة النظام"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "0.1.0-alpha"
    assert "منظومة رشاد AI تعمل بنجاح" in data["message_ar"]
