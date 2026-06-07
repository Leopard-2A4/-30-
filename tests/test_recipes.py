def test_create_recipe(client):
    payload = {
        "name": "something",
        "time_in_minutes": 1,
        "list_of_components": ["something"],
        "documentation": "something",
    }

    response = client.post("/recipes", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["time_in_minutes"] == payload["time_in_minutes"]
    assert data["documentation"] == payload["documentation"]
    assert data["list_of_components"] == payload["list_of_components"]


def test_get_recipes(client):
    payload = {
        "name": "something",
        "time_in_minutes": 1,
        "list_of_components": ["something"],
        "documentation": "something",
    }

    client.post("/recipes", json=payload)

    response = client.get("/recipes")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_recipe_by_id(client):
    payload = {
        "name": "something",
        "time_in_minutes": 1,
        "list_of_components": ["something"],
        "documentation": "something",
    }

    created = client.post("/recipes", json=payload)
    recipe_id = created.json()["id"]

    response = client.get(f"/recipes/{recipe_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == recipe_id
    assert data["name"] == payload["name"]
    assert data["list_of_components"] == payload["list_of_components"]