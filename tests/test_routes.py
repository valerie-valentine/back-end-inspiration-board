from app.models.board import Board
from app.models.card import Card
import pytest

# Test for post_card_to_board route
def test_post_card_to_board(client):
    # Arrange
    board_id = 1
    card_data = {"message": "Test card"}

    # Act
    response = client.post(f"/boards/{board_id}/cards", json=card_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "message" in response_body
    assert response_body["message"] == card_data["message"]

def test_read_all_cards(client):
    response = client.get("/cards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert isinstance(response_body, list)

def test_read_cards_for_board(client, one_card):
    # Arrange
    board_id = 1

    # Act
    response = client.get(f"/boards/{board_id}/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert isinstance(response_body, list)
