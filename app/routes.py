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
    cards_response.sort(key=lambda x: x["id"])
    return jsonify(cards_response), 200

    

#DELETE /cards/1
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_model(Card, card_id)
    db.session.delete(card)
    db.session.commit()

    return jsonify({"details": f'Card {card_id} successfully deleted'}),200

#PATCH /cards/1
@cards_bp.route("/<card_id>/increase_likes", methods=["PATCH"])
def increase_card_likes_count(card_id):
    card_id = int(card_id)
    card = Card.query.get(card_id)
    card.likes_count += 1 
    db.session.commit()
    return jsonify({"card":card.to_dict()}),200

@cards_bp.route("/<card_id>/decrease_likes", methods=["PATCH"])
def decrease_card_likes_count(card_id):
    card_id = int(card_id)
    card = Card.query.get(card_id)
    card.likes_count -= 1 
    db.session.commit()
    return ({"card":card.to_dict()}),200

#PATCH /cards/1
@cards_bp.route("/<card_id>/message", methods=["PATCH"])
def update_card_message(card_id):
    card_data = request.get_json()
    card_id = int(card_id)
    card = Card.query.get(card_id)
    card.message = card_data["message"]
    db.session.commit()
    return jsonify({"card":card.to_dict()}),200


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


# DELETE /boards/1
@boards_bp.route("/<board_id>", methods=["DELETE"])
def delete_board(board_id):
    board = validate_model(Board, board_id)
    db.session.delete(board)
    db.session.commit()

    return jsonify({"details": f'Board {board_id} successfully deleted'}), 200



