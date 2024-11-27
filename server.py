import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from urllib.parse import quote
import re
import time
import random
import openai
import os
from openai import OpenAI
client = OpenAI(
    project='proj_Ae4DRM4LfOvsBwmuXUvqZwPr',
    api_key = os.environ.get("OPENAI_API_KEY"),
)

app = Flask(__name__, static_folder="static")
CORS(app, resources={r"/search": {"origins": "*"}})

limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)

@app.route("/")
def serve_frontend():
    return send_from_directory("templates", "newidea.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        data = request.get_json()
        posts = data.get("posts", [])
        search_type = data.get("type", "travel").strip().lower() 

        if not posts:
            return jsonify({"error": "No posts provided for summarization."}), 400

        content = ""
        for post in posts:
            title = post.get("title", "")
            comments = post.get("top_comments", [])
            post_text = post.get("selftext", "")

            content += f"Title: {title}\n"
            if post_text:
                content += f"Post: {post_text}\n"
            if comments:
                content += "Comments:\n" + "\n".join(f"- {comment}" for comment in comments) + "\n"
            content += "\n"

        if search_type == "travel":
            instruction = (
                "Analyze the posts and comments provided and provide max 10 bullet points with the best things to do and see ONLY IN THE SPECIFIED AREA, with MAX 1000 characters TOTAL (no #,* characters)."
                "Base your response ONLY on the posts' data where available, if there is limited data, can supplement with general knowledge if necessary." 
                "maybe throw in a 2-4 sentence summary at the end after the bullet points of the area."
                
            )
        elif search_type == "food":
            instruction = (
                "Analyze the posts and comments provided and create a summary of the best places to eat or nightlife. ONLY IN THE SPECIFIED AREA with MAX 1000 characters TOTAL, like please keep it kinda short (no #,* characters)."
                "in the area, as well as the best dishes or food in the region or country. Use post data if available; otherwise, supplement with general knowledge if necessary."
            )
        elif search_type == "budget":
            instruction = (
                "Analyze the posts and comments provided and list the cheapest accommodations, such as hostels, along with general money-saving tips for the area. ONLY IN THE SPECIFIED AREA with MAX 1000 characters TOTAL, like please keep it kinda short (no #,* characters)."
                "Try to use post data as much as possible if available; otherwise, supplement with general knowledge if need be."                
            )
        else:
            return jsonify({"error": "Invalid search type provided."}), 400

        response = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[
                {"role": "system", "content": "You are an expert travel assistant."},
                {"role": "user", "content": f"{instruction}\n\n{content}"},
            ],
            temperature=0.5,
        )

        summary = response.choices[0].message.content.strip()
        return jsonify({"summary": summary})

    except Exception as e:
        print("Error in /summarize:", str(e))
        return jsonify({"error": str(e)}), 500
    
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="AuthenticAdventuresapp")
current_time = time.time()
eight_years_in_seconds = 8 * 365 * 24 * 60 * 60

google_headers = {"User-Agent": "AuthenticTravelApp/0.1"}
@app.route("/search", methods=["GET"])
@limiter.limit("8 per minute")
def search():
    try:
        query = request.args.get("q", "").strip()
        search_type = request.args.get("type", "travel").strip().lower()  # travel, food, or budget
        if not query:
            return jsonify({"error": "Query parameter is required."}), 400

        headers = {"User-Agent": "AuthenticTravelApp/0.1"}

        from geopy.geocoders import Nominatim
        geolocator = Nominatim(user_agent="AuthenticAdventuresApp")
        location = geolocator.geocode(query, addressdetails=True, language='en')
        country_name = location.raw.get("address", {}).get("country", "").lower() if location else None

        if search_type == "food":
            keywords = [
                "food", "restaurants", "bar", "nightlife", "pubs", "local dishes",
                "street food", "cuisine", "club", "drink", "night market"
            ]
        elif search_type == "budget":
            keywords = [
                "budget", "cheap", "affordable", "hostel", "free",
                "money-saving", "backpack", "deal", "cheap eats", "money"
            ]
        else:  # Default to travel
            keywords = [
                "itinerary", "guide", "things to do", "trip", "recommendations",
                "hidden gems", "attractions", "adventures", "must-see", "excursions"
            ]
        keyword_pattern = re.compile('|'.join(re.escape(kw) for kw in keywords), re.IGNORECASE)
        exclude_words = ["pic", "picture", "video", "photo"]
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
        specific_subreddit_exists = False
        specific_subreddit_url = f"https://www.reddit.com/r/{quote(query)}/about.json"
        try:
            response = requests.get(specific_subreddit_url, headers=headers)
            if response.status_code == 200:
                specific_subreddit_exists = True
        except requests.exceptions.RequestException:
            pass

        location_posts = []
        if specific_subreddit_exists:
            keywords_query = ' OR '.join(f'"{kw}"' for kw in keywords)
            location_search_url = f"https://www.reddit.com/r/{quote(query)}/search.json?q={quote(keywords_query)}&restrict_sr=1&limit=100&sort=top"
            try:
                response = requests.get(location_search_url, headers=headers)
                response.raise_for_status()
                location_data = response.json()
                location_posts = [post["data"] for post in location_data.get("data", {}).get("children", [])]
            except requests.exceptions.RequestException:
                pass
        general_subreddits = ["travel", "solotravel", "travelnopics"]
        if country_name:
            general_subreddits.append(country_name)

        keywords_query = ' OR '.join(f'"{kw}"' for kw in keywords)
        general_search_query = f'title:"{query}" ({keywords_query})' 
        general_search_url = f"https://www.reddit.com/r/{'+'.join(general_subreddits)}/search.json?q={quote(general_search_query)}&restrict_sr=1&limit=100&sort=top"
        general_posts = []
        try:
            response = requests.get(general_search_url, headers=headers)
            response.raise_for_status()
            general_data = response.json()
            general_posts = [post["data"] for post in general_data.get("data", {}).get("children", [])]
        except requests.exceptions.RequestException:
            pass
        filtered_location_posts = filter_posts(location_posts)[:4]  
        filtered_general_posts = filter_posts(general_posts)[:8] 

        top_posts = filtered_location_posts + filtered_general_posts
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
    port = int(os.environ.get("PORT", 5001))  # Default local port
    app.run(host="0.0.0.0", port=port)