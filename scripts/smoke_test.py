from fastapi.testclient import TestClient
from api.main import app
client=TestClient(app)
response=client.get('/health')
assert response.status_code==200
print(response.json())
