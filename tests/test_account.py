from app import app


def test_failed_field_must_be_include():
    with app.test_client() as c:
        response = c.post("/accounts", json={
            "name": "Joko Santoso",
            "email": "jokojokojoko@gmail.com",
            "phone_number": ""
        })

        assert response.get_json()["msg"] == "fields date_of_birthday must be include"
        assert response.status_code == 400


def test_failed_wrong_format_email():
    with app.test_client() as c:
        response = c.post("/accounts", json={
            "name": "Joko",
            "email": "mantab",
            "phone_number": "",
            "date_of_birthday": "07 01 1998"
        })

        assert response.get_json()["msg"] == "Email Not Valid"
        assert response.status_code == 400


def test_failed_get_account_by_id():
    response = app.test_client().get("/accounts/123456")

    assert response.status_code == 404


def test_success_get_account_by_id():
    response = app.test_client().get("/accounts/1")

    results = [response.get_json()]

    assert len(results) == 1
    assert response.status_code == 200
