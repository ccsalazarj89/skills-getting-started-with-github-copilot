from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture(autouse=True)
def reset_activities():
    original = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


def test_unregister_participant_removes_from_activity():
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200
    assert email in activities[activity_name]["participants"]

    delete_response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    assert delete_response.status_code == 200
    assert email not in activities[activity_name]["participants"]
