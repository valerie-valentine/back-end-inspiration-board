from flask import Blueprint, request, jsonify, make_response, abort
from app.models.card import Card
from app.models.board import Board
from app import db

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")
boards_bp = Blueprint("boards", __name__, url_prefix="/boards")


#helper functions
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"{message":f"{cls.__name__} {model_id} invalid"}, 400))
            
    model = cls.query.get(model_id)
    
    if not model: 
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

# Card routes
#POST /cards
@cards_bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json()
    if ("message" not in request_body or "likes_count" not in request_body):
        abort(make_response({"details": "Invalid data"},400))

    new_card = Card(
        message=request_body["message"],
        likes_count=request_body["likes_count"],
        # completed_at=request_body["completed_at"]
    )

    db.session.add(new_card)
    db.session.commit()

    return jsonify({"card":new_card.to_dict()}),201


@boards_bp.route("/<board_id>/cards", methods=["POST"])
def post_card_to_board(board_id):
    board = validate_model(Board, board_id)

    card_data = request.get_json()
    if "message" not in card_data:
        return jsonify({"message": "Invalid card data"}), 400

    new_card = Card(message=card_data["message"], likes_count=0)
    board.cards.append(new_card)

    db.session.add(new_card)
    db.session.commit()

    return jsonify(new_card.to_dict()), 201

#POST /1/cards
# @boards_bp.route("/<board_id>/cards", methods=["POST"])
# def post_card_to_board(board_id):
#     board = validate_model(Board, board_id)
#     cards_to_add = request.get_json()
#     new_cards_to_add_board = []

#     for card_id in cards_to_add["card_ids"]:
#         new_card = validate_model(Card, card_id)
#         new_cards_to_add_board.append(new_card)
    
#     board.cards= new_cards_to_add_board
#     db.session.commit()

#     return make_response({
#         "id": board.board_id,
#         "card_ids": [card.card_id for card in board.cards]
#     },200)

#GET /cards 
@cards_bp.route("", methods=["GET"])
def read_all_cards():
    cards_query= Card.query
    cards = cards_query.all()
    cards_response = [card.to_dict() for card in cards]
    return jsonify(cards_response)

#GET/ boards/1/cards
@boards_bp.route("/<board_id>/cards", methods=["GET"])
def read_cards_for_board(board_id):
    board = validate_model(Board, board_id)
    cards = board.cards
    cards_response = [card.to_dict() for card in cards]
    return jsonify(cards_response), 200

#DELETE /cards/1
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_model(Card, card_id)
    db.session.delete(card)
    db.session.commit()

    return jsonify({"details": f'Card {card_id} "{card.card_id}" successfully deleted'}),200

#PATCH /cards/1
@cards_bp.route("/<card_id>", methods=["PATCH"])
def update_card(card_id):
    card_id = int(card_id)
    card = Card.query.get(card_id)
    print(card.likes_count)
    request_body = request.get_json()
    card.likes_count = request_body["likes_count"]
    db.session.commit()

    return jsonify({"likes_count":card.likes_count}),200

#Board routes
#POST / boards
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    if "title" not in request_body:
        abort(make_response({"details": "Invalid data"},400))
    
    new_board=Board.from_dict(request_body)
    db.session.add(new_board)
    db.session.commit()

    return jsonify({"board":new_board.to_dict()}),201

#GET/ boards/1
@boards_bp.route("/<board_id>", methods=["GET"])
def read_one_board(board_id):
    board= validate_model(Board, board_id)
    return jsonify({"board":board.to_dict()}),200

#GET/ boards
@boards_bp.route("", methods=["GET"])
def read_all_boards():
    boards = Board.query.all()
    boards_response = [board.to_dict() for board in boards]
    return jsonify(boards_response), 200


