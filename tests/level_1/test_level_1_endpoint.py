import json


def test_endpoint_with_simple_log(level_1_client):
    response = level_1_client.post("/", json={"log": "id=my_id key=value"})
    assert response.status_code == 200

    with open("./parsed/#my_id.json") as f:
        parsed_log = json.load(f)

    assert parsed_log == {"key": "value", "id": "my_id"}


def test_endpoint_with_reference_log(level_1_client):
    response = level_1_client.post(
        "/",
        json={
            "log": "id=0060cd38-9dd5-4eff-a72f-9705f3dd25d9 service_name=api process=api.233 sample#load_avg_1m=0.849 "
            "sample#load_avg_5m=0.561 sample#load_avg_15m=0.202"
        },
    )
    assert response.status_code == 200

    with open("./parsed/#0060cd38-9dd5-4eff-a72f-9705f3dd25d9.json") as f:
        parsed_log = json.load(f)

    assert parsed_log == {
        "id": "0060cd38-9dd5-4eff-a72f-9705f3dd25d9",
        "service_name": "api",
        "process": "api.233",
        "load_avg_1m": "0.849",
        "load_avg_5m": "0.561",
        "load_avg_15m": "0.202",
    }


def test_endpoint_with_error_log(level_1_client):
    response = level_1_client.post(
        "/",
        json={
            "log": "id= 0060cd38-9dd5-4eff-a72f-9705f3dd25d9 service_name=api process=api.233 sample#load_avg_1m=0.849 "
            "sample#load_avg_5m=0.561 sample#load_avg_15m=0.202"
        },
    )

    assert response.status_code == 400
