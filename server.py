# server.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/search')
def search():
    location = request.args.get('q')
    if not location:
        return jsonify({'error': 'Missing query parameter q'}), 400

    try:
        url = f'https://www.reddit.com/r/travel/search.json?q={location}&restrict_sr=1'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        data = response.json()
        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to fetch data from Reddit'}), 500

if __name__ == '__main__':
    app.run(debug=True)
