import pytest
from app import create_app
from app import db
from app.models.board import Board
from app.models.card import Card
from flask.signals import request_finished



@pytest.fixture
def app():
    # create the app with a test config dictionary
    # app = create_app({"TESTING": True})
    app = create_app()


    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def one_card(app):
    board = Board(title="Test Board")
    card = Card(message="Test Card", likes_count=0)
    
    board.cards.append(card)
    
    db.session.add(board)
    db.session.commit()

    return card

@pytest.fixture
def one_board(app):
    board = Board(title="Test Board", owner="Test Owner") 

    db.session.add(board)
    db.session.commit()

    return board

