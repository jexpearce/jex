from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search_reddit():
    query = request.args.get('q', '')  #search term
    subreddit = request.args.get('subreddit', 'travel')  # travel subreddit
    url = f"https://www.reddit.com/r/{subreddit}/search.json?q={query}&restrict_sr=1"
    headers = {"User-Agent": "Reddit-Search-API"}
    reddit_response = requests.get(url, headers=headers)

    if reddit_response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from Reddit"}), reddit_response.status_code
    return jsonify(reddit_response.json())

if __name__ == '__main__':
    app.run(debug=True)
