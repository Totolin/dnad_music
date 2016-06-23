from flask import Flask, jsonify

def create():
    app = Flask(__name__)

    @app.route('/recommend', methods=['POST'])
    def create_task():
        if not request.json or not 'song' in request.json:
            abort(400)
        
        # request.json contains the "song" key

        # get song recommendations, return 200
        # or return != 200 if there's an error
        tasks.append(task)

        return jsonify({'task': task}), 200

    return app

