from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


#
def test_get_insights_user_not_found():
    response = client.get("/user-insights/usuario_no_existe")
    assert response.status_code == status.HTTP_404_NOT_FOUND
