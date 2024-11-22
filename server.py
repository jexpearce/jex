import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from urllib.parse import quote
import re
import time
import os
import random

app = Flask(__name__, static_folder="static")
CORS(app, resources={r"/search": {"origins": "*"}})

limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)

@app.route("/")
def serve_frontend():
    return send_from_directory("templates", "newidea.html")

@app.route("/search", methods=["GET"])
@limiter.limit("8 per minute")
def search():
    try:
        query = request.args.get("q", "").strip()
        search_type = request.args.get("type", "travel").strip().lower()  # "travel" or "food"
        if not query:
            return jsonify({"error": "Query parameter is required."}), 400

        headers = {"User-Agent": "AuthenticTravelApp/0.1"}

        # checks if the r/[location] even exists
        encoded_query = quote(query)
        specific_subreddit_url = f"https://www.reddit.com/r/{encoded_query}/about.json"
        specific_subreddit_exists = False

        try:
            subreddit_response = requests.get(specific_subreddit_url, headers=headers)
            if subreddit_response.status_code == 200:
                specific_subreddit_exists = True
        except requests.exceptions.RequestException:
            specific_subreddit_exists = False

        # keywords
        if search_type == "food":
            keywords = [
                "food", "culture", "restaurants", "nightlife", "clubs", "bars",
                "pubs", "cocktails", "night market", "places to eat", "local food",
                "must-try dishes", "street food", "cuisine",
            ]
        elif search_type == "budget":
            keywords = ["budget", "cheap", "affordable", "low-cost", "money-saving"]
        else:  #means it will default to the "find travel tips"
            keywords = [
                "itinerary", "guide", "things to do", "trip",
                "recommendations", "must-see",
                "must-visit", "hidden gems", "attractions","excursions",
            ]
        keyword_pattern = re.compile('|'.join(re.escape(kw) for kw in keywords), re.IGNORECASE)
        exclude_words = ["pic", "picture", "pictures", "video", "vid", "photo"]
        exclude_pattern = re.compile('|'.join(re.escape(word) for word in exclude_words), re.IGNORECASE)

        current_time = time.time()
        eight_years_in_seconds = 8 * 365 * 24 * 60 * 60

        def filter_posts(posts):
            return [
                post
                for post in posts
                if keyword_pattern.search(post.get("title", ""))  
                and not exclude_pattern.search(post.get("title", ""))  
                and post.get("post_hint") != "image"
                and not post.get("is_video", False)
                and "media_metadata" not in post
                and current_time - post.get("created_utc", current_time) <= eight_years_in_seconds
            ]

  
        location_posts = []
        if specific_subreddit_exists: 
            keywords_query = ' OR '.join(f'"{kw}"' for kw in keywords)
            encoded_keywords_query = quote(keywords_query)
            location_search_url = f"https://www.reddit.com/r/{encoded_query}/search.json?q={encoded_keywords_query}&restrict_sr=1&limit=100&sort=top"
            try:
                location_response = requests.get(location_search_url, headers=headers)
                location_response.raise_for_status()
                location_data = location_response.json()
                location_posts = [post["data"] for post in location_data.get("data", {}).get("children", [])]
            except requests.exceptions.RequestException:
                pass  

       
        general_subreddits = "travel+travelnopics+solotravel"
        keywords_query = ' OR '.join(f'"{kw}"' for kw in keywords)
        general_search_query = f'title:"{query}" ({keywords_query})'
        encoded_general_search_query = quote(general_search_query)
        general_search_url = f"https://www.reddit.com/r/{general_subreddits}/search.json?q={encoded_general_search_query}&restrict_sr=1&limit=100&sort=top"
        general_posts = []
        try:
            general_response = requests.get(general_search_url, headers=headers)
            general_response.raise_for_status()
            general_data = general_response.json()
            general_posts = [post["data"] for post in general_data.get("data", {}).get("children", [])]
        except requests.exceptions.RequestException:
            pass  

    
        filtered_location_posts = filter_posts(location_posts)
        filtered_general_posts = filter_posts(general_posts)

        top_posts = filtered_location_posts[:5] + filtered_general_posts[:5] 
        random.shuffle(top_posts)  



        for post in top_posts:
            post_id = post.get("id")
            post_subreddit = post.get("subreddit")
            if not post_id or not post_subreddit:
                continue
            comments_url = f"https://www.reddit.com/r/{post_subreddit}/comments/{post_id}.json?depth=1&limit=5"
            try:
                comments_response = requests.get(comments_url, headers=headers)
                comments_response.raise_for_status()
                comments_data = comments_response.json()
                post["top_comments"] = [
                    comment["data"]["body"]
                    for comment in comments_data[1]["data"]["children"]
                    if (
                        comment.get("kind") == "t1"
                        and comment["data"].get("body")
                        and "[deleted]" not in comment["data"]["body"]
                        and "[removed]" not in comment["data"]["body"]
                    )
                ]
            except requests.exceptions.RequestException:
                post["top_comments"] = []

        return jsonify(top_posts)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))  
    app.run(host="0.0.0.0", port=port)
