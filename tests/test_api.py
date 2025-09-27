from api.main import main
import azure.functions as func

def test_api_returns_json():
    req = func.HttpRequest(
        method='GET',
        url='/api/data',
        body=b'',
        headers={}
    )
    resp = main(req)
    assert resp.status_code == 200
    assert 'application/json' in resp.headers['Content-Type']