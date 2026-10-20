import uuid
import requests
BASE_URL = "http://127.0.0.1:5000"

def test_sql_injection_negative():
    payload={"name":"Arman' OR '1'='1","email":f"arman.sql.{uuid.uuid4().hex[:8]}@test.com"}
    r=requests.post(BASE_URL+"/api/users",json=payload)
    assert r.status_code in (201,400)
    users=requests.get(BASE_URL+"/api/users")
    assert users.status_code==200
    assert isinstance(users.json(),list)

def test_xss_negative():
    xss="<script>alert('Arman')</script>"
    payload={"name":xss,"email":f"arman.xss.{uuid.uuid4().hex[:8]}@test.com"}
    r=requests.post(BASE_URL+"/api/users",json=payload)
    assert r.status_code in (201,400)
    if r.status_code==201:
        assert r.json()["name"]==xss
