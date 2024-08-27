from flask import Flask, request, jsonify
from collections.abc import Iterable

app = Flask(__name__)

# Dummy storage 
dislikes = 0
comments = []

@app.route('/feedback/like', methods=['POST'])
def handle_like():
    global likes
    likes += 1
    return jsonify({"message": "Like recorded", "total_likes": likes})

@app.route('/feedback/dislike', methods=['POST'])
def handle_dislike():
    global dislikes
    dislikes += 1
    return jsonify({"message": "Dislike recorded", "total_dislikes": dislikes})

@app.route('feedback/comment', methods=['POST'])
def handle_comment():
    data = request.json
    comment = data.get('comment')
    if comment:
        comments.append(comment)
        return jsonify({"message": "Comment recorded", "total_comments": len(comments)})
    else:
        return jsonify({"error": "No comment provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
