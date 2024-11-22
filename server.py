import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from urllib.parse import quote
import re
import time
import os

app = Flask(__name__, static_folder="static")
CORS(app, resources={r"/search": {"origins": "https://your-frontend-domain.com"}})  # Restrict CORS to your frontend domain
limiter = Limiter(app, key_func=get_remote_address)  # Add rate limiting

@app.route("/")
def serve_frontend():
    return send_from_directory("templates", "newidea.html")

@app.route("/search", methods=["GET"])
@limiter.limit("8 per minute")  # Limit to 8 requests per minute per IP
def search():
    try:
        query = request.args.get("q", "").strip()
        if not query:
            return jsonify({"error": "Query parameter is required."}), 400

        headers = {"User-Agent": "AuthenticTravelApp/0.1"}
        eight_years_in_seconds = 8 * 365 * 24 * 60 * 60
        current_time = time.time()
        keyword_pattern = re.compile('|'.join([
            "itinerary", "guide", "things to do", "plan", "trip",
            "recommendations", "advice", "destinations", "must-see",
            "must-visit", "hidden gems", "attractions", "activities", "excursions",
        ]))

        def filter_posts(data):
            return [
                post["data"]
                for post in data.get("data", {}).get("children", [])
                if keyword_pattern.search(post["data"]["title"].lower())
                and post["data"].get("post_hint") != "image"
                and not post["data"].get("is_video", False)
                and "media_metadata" not in post["data"]
                and current_time - post["data"]["created_utc"] <= eight_years_in_seconds
            ]

        # Check if specific subreddit exists and is accessible
        encoded_query = quote(query)
        specific_subreddit_url = f"https://www.reddit.com/r/{encoded_query}/about.json"
        specific_posts = []

        try:
            subreddit_response = requests.get(specific_subreddit_url, headers=headers)
            if subreddit_response.status_code == 200:
                specific_posts_url = f"https://www.reddit.com/r/{encoded_query}/search.json?q=&restrict_sr=1&limit=100&sort=top"
                specific_posts_response = requests.get(specific_posts_url, headers=headers)
                specific_posts_response.raise_for_status()
                specific_posts = filter_posts(specific_posts_response.json())
                specific_posts = specific_posts[:4]  # Limit to top 4 posts
        except requests.exceptions.RequestException:
            pass  # Ignore errors for restricted or non-existent subreddits

        # Fetch posts from travel-related subreddits
        travel_url = f"https://www.reddit.com/r/travel+travelnopics+solotravel/search.json?q=title%3A{query}&restrict_sr=1&limit=100&sort=top"
        travel_response = requests.get(travel_url, headers=headers)
        travel_response.raise_for_status()
        travel_posts = filter_posts(travel_response.json())
        travel_posts = travel_posts[:4]  # Limit to top 4 posts

        # Combine and prioritize specific subreddit posts
        all_posts = specific_posts + travel_posts

        # Fetch top comments for each post
        for post in all_posts:
            post_id = post["id"]
            post_subreddit = post["subreddit"]
            comments_url = f"https://www.reddit.com/r/{post_subreddit}/comments/{post_id}.json?depth=1&limit=5"
            comments_response = requests.get(comments_url, headers=headers)
            comments_response.raise_for_status()
            comments_data = comments_response.json()

            # Extract and validate comments
            if len(comments_data) > 1:
                comments = [
                    comment["data"]["body"]
                    for comment in comments_data[1].get("data", {}).get("children", [])
                    if (
                        comment.get("kind") == "t1"
                        and comment["data"].get("body")
                        and "[deleted]" not in comment["data"]["body"]
                        and "[removed]" not in comment["data"]["body"]
                    )
                ]
                post["top_comments"] = comments[:5]  # Limit to top 5 comments
            else:
                post["top_comments"] = []

        return jsonify(all_posts)

    except requests.exceptions.RequestException as req_err:
        return jsonify({"error": f"Request error: {str(req_err)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
