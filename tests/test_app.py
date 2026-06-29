from src.app import activities


def test_unregister_participant_removes_from_activity(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    delete_response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert signup_response.status_code == 200
    assert delete_response.status_code == 200
    assert email not in activities[activity_name]["participants"]


def test_duplicate_signup_is_rejected(client):
    # Arrange
    activity_name = "Chess Club"
    email = "existing@mergington.edu"

    # Act
    first_signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    second_signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert first_signup_response.status_code == 200
    assert second_signup_response.status_code == 400
    assert activities[activity_name]["participants"].count(email) == 1
