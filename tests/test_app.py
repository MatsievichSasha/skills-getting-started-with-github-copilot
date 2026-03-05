"""
Tests for the FastAPI backend application.

Uses pytest and FastAPI's TestClient for integration testing.
Each test follows the AAA (Arrange-Act-Assert) pattern.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    """Test GET /activities returns all activities."""
    # Arrange
    expected_activities = activities

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == expected_activities


def test_signup_for_activity_success():
    """Test successful signup for an activity."""
    # Arrange
    activity_name = "Chess Club"
    email = "test@example.com"
    initial_participants = activities[activity_name]["participants"].copy()

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]
    # Clean up
    activities[activity_name]["participants"].remove(email)


def test_signup_for_activity_duplicate():
    """Test signup fails when student is already signed up."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student is already signed up for this activity"}


def test_signup_for_activity_not_found():
    """Test signup fails for non-existent activity."""
    # Arrange
    activity_name = "NonExistent Activity"
    email = "test@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_from_activity_success():
    """Test successful unregister from an activity."""
    # Arrange
    activity_name = "Programming Class"
    email = "test@example.com"
    # First sign up
    activities[activity_name]["participants"].append(email)

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}
    assert email not in activities[activity_name]["participants"]


def test_unregister_from_activity_not_signed_up():
    """Test unregister fails when student is not signed up."""
    # Arrange
    activity_name = "Programming Class"
    email = "notsignedup@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student is not signed up for this activity"}


def test_unregister_from_activity_not_found():
    """Test unregister fails for non-existent activity."""
    # Arrange
    activity_name = "NonExistent Activity"
    email = "test@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}