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

# OpenAI Client Initialization
client = OpenAI(
    project='proj_Ae4DRM4LfOvsBwmuXUvqZwPr',
    api_key=os.environ.get("OPENAI_API_KEY"),
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

        # Original search-type specific instructions
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

        # Use OpenAI to generate the summary
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


# NEW ROUTE: Generate 'n'-day itinerary
@app.route("/generate_itinerary", methods=["POST"])
def generate_itinerary():
    try:
        data = request.get_json()
        query = data.get("location", "").strip()
        days = data.get("days", 1)

        if not query or not days:
            return jsonify({"error": "Location and number of days are required."}), 400

        # Fetch posts using the same search logic
        posts = fetch_reddit_posts(query)

        # Create content for AI
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

        # New instruction specifically for itinerary
        instruction = (
            f"Using the following posts and comments, create a {days}-day travel itinerary for {query}."
            " For each day, recommend specific activities, locations, or experiences based on the posts' details."
            " Keep it detailed and logical, spreading activities across all days where possible."
        )

        # Use OpenAI to generate the itinerary
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert travel assistant."},
                {"role": "user", "content": f"{instruction}\n\n{content}"},
            ],
            temperature=0.7,
        )

        itinerary = response.choices[0].message.content.strip()
        return jsonify({"itinerary": itinerary, "posts": posts})

    except Exception as e:
        print("Error in /generate_itinerary:", str(e))
        return jsonify({"error": str(e)}), 500


# HELPER FUNCTION: Fetch Reddit posts (reusable for all routes)
def fetch_reddit_posts(query):
    headers = {"User-Agent": "AuthenticTravelApp/0.1"}
    current_time = time.time()
    eight_years_in_seconds = 8 * 365 * 24 * 60 * 60

    # Fetch posts
    search_url = f"https://www.reddit.com/search.json?q={quote(query)}&limit=50"
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        posts = [
            post["data"] for post in data.get("data", {}).get("children", [])
            if current_time - post["data"].get("created_utc", current_time) <= eight_years_in_seconds
        ]
    except requests.exceptions.RequestException:
        posts = []

    # Enrich posts with comments
    for post in posts:
        post_id = post.get("id")
        subreddit = post.get("subreddit")
        comments_url = f"https://www.reddit.com/r/{subreddit}/comments/{post_id}.json?depth=1&limit=5"
        try:
            comments_response = requests.get(comments_url, headers=headers)
            comments_response.raise_for_status()
            comments_data = comments_response.json()
            post["top_comments"] = [
                comment["data"]["body"] for comment in comments_data[1]["data"]["children"]
                if comment["data"].get("body") not in ["[deleted]", "[removed]"]
            ]
        except:
            post["top_comments"] = []

    return posts


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))  # Default local port
    app.run(host="0.0.0.0", port=port)
