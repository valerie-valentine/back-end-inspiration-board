from app.models.board import Board
from app.models.card import Card
import pytest

#Tests for card routes

def test_post_card_to_board(client, one_card):
    # Arrange
    board_id = one_card.board.board_id
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

def test_delete_card(client, one_card):
    # Prepare
    card_id = one_card.card_id

    # Act
    response = client.delete(f"/cards/{card_id}")

    # Assert
    assert response.status_code == 200

def test_update_card(client, one_card):
    # Prepare
    card_id = one_card.card_id
    new_likes_count = 10
    update_data = {"likes_count": new_likes_count}

    # Act
    response = client.patch(f"/cards/{card_id}", json=update_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "likes_count" in response_body
    assert response_body["likes_count"] == new_likes_count

def test_create_board(client, one_board):
    # Arrange
    board_data = {
        "title": "Test Board",
        "owner": "Test Owner"  
    }

    # Act
    response = client.post("/boards", json=board_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "board" in response_body
    assert "title" in response_body["board"]
    assert response_body["board"]["title"] == "Test Board"
    assert "owner" in response_body["board"]
    assert response_body["board"]["owner"] == "Test Owner"

def test_read_one_board(client, one_board):
    # Arrange
    board_id = one_board.board_id

    # Act
    response = client.get(f"/boards/{board_id}")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "board" in response_body
    assert "title" in response_body["board"]
    assert response_body["board"]["title"] == one_board.title

def test_read_all_boards(client, one_board):
    # Arrange
    board_title = one_board.title

    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert isinstance(response_body, list)
    assert any(board["title"] == board_title for board in response_body)