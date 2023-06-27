from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from flask import jsonify
from flask import abort

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

# create a new card
@cards_bp.route("", methods =["POST"])
def create_card():
    request_body = request.get_json()
    new_card = Card(
        body=request_body["body"],
        likes=request_body["likes"])

    db.session.add(new_card)
    db.session.commit()

    return make_response(f"Card {new_card.body} created")
