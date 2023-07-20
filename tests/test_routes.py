from app.models.board import Board
from app.models.card import Card
import pytest
import uuid

# Tests for card routes

def test_post_card_to_board(client, one_board):
    # Act
    response = client.post(f"/boards/{one_board.board_id}/cards", json={
        "message": 'Test Card'
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "id" in response_body
    assert "message" in response_body
    assert response_body["message"] == 'Test Card'

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

def test_increase_card_likes_count(client, one_card):
    # Arrange
    card_id = one_card.card_id
    initial_likes_count = one_card.likes_count

    # Act
    response = client.patch(f"/cards/{card_id}/increase_likes")

    # Assert
    assert response.status_code == 200
    response_data = response.get_json()  
    assert "card" in response_data
    assert "likes_count" in response_data["card"]
    assert response_data["card"]["likes_count"] == initial_likes_count + 1



def test_create_board(client):
    # Arrange
    board_id = str(uuid.uuid4())
    board_data = {
        "board_id": board_id,
        "title": "Test Board",
        "owner": "Test Owner",
        "image": "Image"  
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