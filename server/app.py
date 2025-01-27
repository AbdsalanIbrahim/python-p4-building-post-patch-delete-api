#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

@app.route('/games')
def games():
    games = [game.to_dict() for game in Game.query.all()]
    
    if not games:
        return make_response(
            {"message": "No games available"},
            404
        )

    return make_response(games, 200)

@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    
    if not game:
        return make_response(
            {"error": "Game not found"}, 
            404
        )

    game_dict = game.to_dict()

    response = make_response(
        game_dict,
        200
    )

    return response

@app.route('/reviews')
def reviews():
    reviews = [review.to_dict() for review in Review.query.all()]
    
    if not reviews:
        return make_response(
            {"message": "No reviews available"},
            404
        )

    return make_response(reviews, 200)

@app.route('/users')
def users():
    users = [user.to_dict() for user in User.query.all()]
    
    if not users:
        return make_response(
            {"message": "No users available"},
            404
        )

    return make_response(users, 200)

@app.errorhandler(404)
def not_found(error):
    return make_response({"error": "Resource not found"}, 404)

@app.errorhandler(500)
def internal_error(error):
    return make_response({"error": "Internal server error"}, 500)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
