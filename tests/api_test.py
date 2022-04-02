import requests
import json
from jsonschema import validate
from jsonschema import Draft6Validator

base_url = 'http://127.0.0.1:9000'


def test_calculate_price_api():

    api_input = {
                 "rate": { "energy": 0.3, "time": 2, "transaction": 1 },
                 "cdr": { "meterStart": 1204307, "timestampStart": "2021-04-05T10:04:00Z", "meterStop": 1215230.5, "timestampStop": "2021-04-05T11:27:00Z" }
                }
    response = requests.post(base_url + '/calculate-price', json=api_input)
    resp_body = response.json()
    # Validate response headers and body contents, e.g. status code.
    assert response.status_code == 200

    # Validate response content type header
    assert response.headers["Content-Type"] == "application/json"

    assert resp_body['overall'] == 7.04
    # Validate will raise exception if given json is not
    # what is described in schema.
    # validate(instance=resp_body, schema=schema)


def test_update_rate():

    api_input = { "stationId": 1, "energy": 0.3, "time": 2, "transaction": 1}

    response = requests.post(base_url + '/update_rates', json=api_input)
    resp_body = response.json()
    # Validate response headers and body contents, e.g. status code.
    assert response.status_code == 200

    # Validate response content type header
    assert response.headers["Content-Type"] == "application/json"

    assert resp_body['status'] == True
    # Validate will raise exception if given json is not
    # what is described in schema.
    # validate(instance=resp_body, schema=schema)


if __name__ == '__main__':
    test_calculate_price_api()