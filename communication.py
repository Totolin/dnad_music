from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import utils

# Holder for the engine
analyzer = None

def create(engine):
    # Create Flask application
    app = Flask(__name__)

    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    # Save analyzer engine
    analyzer = engine

    @app.route('/recommend', methods=['POST'])
    def create_task():
        print request.json
        if not request.json or not 'song' in request.json:
            abort(400)
        
        if not isinstance(request.json["song"], basestring):
            abort(400)

        # Get the song name to be searched
        songname = request.json["song"]

        # Tell engine to recommend 5 songs
        songs = analyzer.recommend(songname)

        return jsonify(songs), 200

    return app

