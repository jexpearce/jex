import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/search", methods=["GET"])
def search():
    try:
        query = request.args.get("q", "")
        if not query:
            return jsonify({"error": "Query parameter is required."}), 400

        # Combine the three subreddits
        url = f"https://www.reddit.com/r/travel+travelnopics+solotravel/search.json?q=title%3A{query}&restrict_sr=1&limit=100&sort=top"
        headers = {"User-Agent": "AuthenticTravelApp/0.1"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Check if data structure is as expected
        if "data" not in data or "children" not in data["data"]:
            return jsonify({"error": "Unexpected Reddit API response structure."}), 500

        # Keywords for filtering posts
        keywords = [
            "itinerary",
            "guide",
            "things to do",
            "plan",
            "trip",
            "recommendations",
            "advice",
            "destinations",
            "must-see",
            "must-visit",
            "hidden gems",
            "attractions",
            "activities",
            "excursions",
        ]

        # Create a regex pattern for keywords
        keyword_pattern = re.compile('|'.join(re.escape(kw) for kw in keywords))

        # Filter posts based on title containing keywords
        filtered_posts = [
            post["data"]
            for post in data["data"]["children"]
            if keyword_pattern.search(post["data"]["title"].lower())
            and post["data"].get("post_hint") != "image"  # Exclude image posts
            and not post["data"].get("is_video", False)  # Exclude video posts
            and "media_metadata" not in post["data"]  # Exclude gallery posts
        ]

        # Limit to the top 5 posts
        top_posts = filtered_posts[:5]

        # For each post, fetch top 5 comments inline
        for post in top_posts:
            post_id = post["id"]
            post_subreddit = post["subreddit"]  # Specific subreddit for this post
            comments_url = f"https://www.reddit.com/r/{post_subreddit}/comments/{post_id}.json?depth=1&limit=5"
            comments_response = requests.get(comments_url, headers=headers)
            comments_response.raise_for_status()
            comments_data = comments_response.json()

            # Validate comments_data structure
            if len(comments_data) < 2 or "data" not in comments_data[1] or "children" not in comments_data[1]["data"]:
                post["top_comments"] = []
                continue

            # Extract comments, excluding [deleted] or large comments
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

        return jsonify(top_posts)

    except requests.exceptions.RequestException as req_err:
        return jsonify({"error": f"Request error: {str(req_err)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5001)
