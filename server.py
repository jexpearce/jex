import requests
from flask import Flask, request, jsonify, send_from_directory, session
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
    api_key=os.environ.get("OPENAI_API_KEY"),
)

app = Flask(__name__, static_folder="static")
app.secret_key = os.urandom(24)  
CORS(app, resources={r"/search": {"origins": "*"}})

limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)

def get_posts_by_ids(post_ids, query, search_type="travel"):
    """Fetch posts by their IDs"""
    posts = fetch_reddit_posts(query, search_type)
        # Filter posts to only those with matching IDs
    return [post for post in posts if post.get("id") in post_ids]


@app.route("/")
def serve_frontend():
    return send_from_directory("templates", "newidea.html")


def fetch_reddit_posts(query, search_type):
    google_headers = {"User-Agent": "AuthenticTravelApp/0.1"}
    current_time = time.time()
    eight_years_in_seconds = 8 * 365 * 24 * 60 * 60
    seen_ids = set()
    all_posts = []

    def normalize_location(loc):
        no_space = loc.replace(" ", "")
        return [no_space, loc] if " " in loc else [loc]

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
    else: 
        keywords = [
            "itinerary", "guide", "things to do", "trip", "recommendations", "stuff to do",
            "hidden gems", "attractions", "adventures", "must see", "excursions", "what to do"
        ]
    keyword_pattern = re.compile('|'.join(re.escape(kw) for kw in keywords), re.IGNORECASE)
    exclude_words = ["pic", "picture", "video", "photo"]
    exclude_pattern = re.compile('|'.join(re.escape(word) for word in exclude_words), re.IGNORECASE)

    def filter_posts(posts, is_location_specific_subreddit=False):
        filtered = []
        for post in posts:
            if post.get("id") in seen_ids:
                continue

            title = post.get("title", "").lower()
            
            if (post.get("post_hint") == "image" or 
                post.get("is_video", False) or 
                "media_metadata" in post or 
                current_time - post.get("created_utc", current_time) > eight_years_in_seconds or
                exclude_pattern.search(title)):
                continue

            # Different filtering for location-specific vs general subreddits
            if is_location_specific_subreddit==True:
                # Only need to match activity keywords
                if keyword_pattern.search(title):
                    filtered.append(post)
            elif is_location_specific_subreddit==False:
                if keyword_pattern.search(title) and query.lower() in title.lower():
                    filtered.append(post)
                    
        return filtered

    def add_limited_posts(posts, max_posts):
        sorted_posts = sorted(posts, key=lambda x: x.get("ups", 0), reverse=True)
        added = 0
        for post in sorted_posts:
            if added >= max_posts:
                break
            if post.get("id") not in seen_ids:
                seen_ids.add(post.get("id"))
                all_posts.append(post)
                added += 1
        return added
    
    # 1. First check location-specific subreddit (max 6 posts)
    try:
        location_variants = normalize_location(query)
        for variant in location_variants:
            location_subreddit_url = f"https://www.reddit.com/r/{quote(variant)}/about.json"
            response = requests.get(location_subreddit_url, headers=google_headers)
            if response.status_code == 200:
                search_url = f"https://www.reddit.com/r/{quote(variant)}/search.json?q={quote(' OR '.join(keywords))}&restrict_sr=1&limit=100&sort=top"
                try:
                    response = requests.get(search_url, headers=google_headers)
                    if response.status_code == 200:
                        data = response.json()
                        posts = [post["data"] for post in data.get("data", {}).get("children", [])]
                        filtered_posts = filter_posts(posts, is_location_specific_subreddit=True)
                        add_limited_posts(filtered_posts, 6)
                        break  # Stop after finding first valid subreddit
                except requests.exceptions.RequestException:
                    pass
    except requests.exceptions.RequestException:
        pass

    # 3. Check general travel subreddits for remaining slots
    general_subreddits = ["travel", "solotravel", "travelnopics"]
    posts_needed = 16 - len(all_posts)
    
    if posts_needed > 0:
        for subreddit in general_subreddits:
            search_url = f"https://www.reddit.com/r/{subreddit}/search.json?q={quote(query)}&restrict_sr=1&limit=100&sort=top"
            try:
                response = requests.get(search_url, headers=google_headers)
                if response.status_code == 200:
                    data = response.json()
                    posts = [post["data"] for post in data.get("data", {}).get("children", [])]
                    filtered_posts = filter_posts(posts, is_location_specific_subreddit=False)
                    add_limited_posts(filtered_posts, posts_needed)
            except requests.exceptions.RequestException:
                pass 

    # Final sort by upvotes
    return sorted(all_posts, key=lambda x: x.get("ups", 0), reverse=True)
@app.route("/search", methods=["GET"])
@limiter.limit("8 per minute")
def search():
    try:
        query = request.args.get("q", "").strip()
        search_type = request.args.get("type", "travel").strip().lower()  # travel, food, or budget
        if not query:
            return jsonify({"error": "Query parameter is required."}), 400

        posts = fetch_reddit_posts(query, search_type)


        headers = {"User-Agent": "AuthenticTravelApp/0.1"}
        for post in posts:
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

        session["cached_post_ids"] = [post.get("id") for post in posts]
        session["cached_query"] = query

        return jsonify(posts)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
                "Analyze the posts and comments provided and provide max 10 bullet points with the best things to do and see ONLY IN THE SPECIFIED AREA, with MAX 1000 characters TOTAL"
                "Base your response ONLY on the posts' data where available, if there is limited data, can supplement with general knowledge if necessary."
                "Format each bullet point with <br> after it for line breaks. Start each bullet with a • character."
                "After bullet points, add <br><br> followed by a 2-4 sentence summary." 
            )
        elif search_type == "food":
            instruction = (
                "Analyze the posts and comments provided and create a summary of the best places to eat or nightlife. ONLY IN THE SPECIFIED AREA with MAX 1000 characters TOTAL, like please keep it kinda short "
                "in the area, as well as the best dishes or food in the region or country. Use post data if available; otherwise, supplement with general knowledge if necessary."
                "Use bullet points of places to eat/nightlife if you have enough data, then can do a separate bullet point list for the best food in that region MAX 5 bullet points for food."
                "Format each bullet point with <br> after it for line breaks. Start each bullet with a • character."
                "After bullet points, add <br><br> followed by a 2-4 sentence summary." 
            )
        elif search_type == "budget":
            instruction = (
                "Analyze the posts and comments provided and list the cheapest accommodations, such as hostels, along with general money-saving tips for the area. ONLY IN THE SPECIFIED AREA with MAX 1000 characters TOTAL, like please keep it kinda short."
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



@app.route("/generate_itinerary", methods=["POST"])
def generate_itinerary():
    try:
        data = request.get_json()
        query = data.get("location", "").strip()
        days = data.get("days", 1)

        if not query or not days:
            return jsonify({"error": "Location and number of days are required."}), 400

        cached_query = session.get("cached_query")
        cached_post_ids = session.get("cached_post_ids", [])
        if cached_query == query and cached_post_ids:
            posts = get_posts_by_ids(cached_post_ids, query)
        else:
            try:
                posts = fetch_reddit_posts(query, "travel")
                #only cache if successful
                session["cached_query"] = query
                session["cached_post_ids"] = [post.get("id") for post in posts]
            except Exception as e:
                #clear it on error to stop it from always getting stuck
                session.pop("cached_query", None)
                session.pop("cached_post_ids", None)
                raise e

            headers = {"User-Agent": "AuthenticTravelApp/0.1"}
            for post in posts:
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

            session["cached_query"] = query
            session["cached_post_ids"] = [post.get("id") for post in posts]


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

        instruction = (
            f"Using the following posts and comments only, create a {days}-day travel itinerary for {query}, maximum 800 characters (and no #,* characters)."
            " For each day, recommend specific activities, locations, or experiences based on the posts and comments details only. Only iff there is limited info (not many relevant posts/comments), feel free to supplement with suggestions that you know of."
            " Format each day as '<strong>Day X:</strong><br>' and each activity as '• Activity<br>'."
            " Add <br> between days for spacing."
            " Start with '<strong>{days}-day itinerary in {query}</strong><br><br>'."
            "do NOT add a summary of the area or how to get there (e.g., from the airport)."
        )

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



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))  
    app.run(host="0.0.0.0", port=port)
