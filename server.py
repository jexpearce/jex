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

# Location to subreddit mappings
LOCATION_MAPPINGS = {
    # Southeast Asia
    "vietnam": ["VietNam", "hanoi", "hochiminh", "saigon", "da nang"],
    "thailand": ["thailand", "bangkok", "chiang mai","phuket"],
    # "singapore": ["singapore"],
    # "indonesia": ["indonesia", "bali", "jakarta","bromo","yogyakarta","sulawesi","sumatra","lombok"],
     "laos": ["laos","vangvieng","luangprabang", "vientiane", "pakse"],
     "cambodia": ["cambodia","siemreap","angkorwat", "phnompenh", "kohrong"],
     "malaysia": ["malaysia","kualalumpur","langkawi", "penang"],
    # "philippines": ["philippines", "manila", "cebu", "boracay", "palawan", "bohol", "siargao"],
    
    # Europe
    # "france": ["france", "paris", "lyon", "nice", "marseille", "bordeaux", "lille", "strasbourg", "nantes", "toulouse", "cannes", "montpellier", "avignon", "annecy"],
    # "spain": ["spain", "barcelona", "madrid", "seville", "granada", "malaga", "valencia", "bilbao", "toledo", "sansebastian", "cordoba", "zaragoza", "tenerife", "mallorca", "ibiza"],
    # "italy": ["italy", "rome", "venice", "florence", "milan", "naples", "pisa", "bologna", "sicily", "sardinia", "cinqueterre", "verona", "turin", "amalfi"],
    # "germany": ["germany", "berlin", "munich", "hamburg", "frankfurt", "dresden", "stuttgart", "cologne", "nuremberg", "heidelberg", "leipzig", "hanover", "bremen"],
    # "unitedkingdom": ["unitedkingdom", "england", "london", "edinburgh", "glasgow", "manchester", "birmingham", "bath", "york", "cambridge", "oxford", "cardiff", "belfast"],
    # "greece": ["greece", "athens", "santorini", "mykonos", "crete", "thessaloniki", "rhodes", "corfu", "delphi", "olympia"],
    # "portugal": ["portugal", "lisbon", "porto", "algarve", "sintra", "madeira", "azores", "coimbra"],
    # "netherlands": ["netherlands", "amsterdam", "rotterdam", "utrecht", "thehague", "delft", "maastricht"],
    # "switzerland": ["switzerland", "zurich", "geneva", "lucerne", "interlaken", "zermatt", "bern", "grindelwald", "lausanne"],
    # "austria": ["austria", "vienna", "salzburg", "innsbruck", "hallstatt", "graz", "linz"],
    # "belgium": ["belgium", "brussels", "bruges", "ghent", "antwerp", "liege"],
    # "czech": ["czechia", "prague", "ceskykrumlov", "brno", "karlovyvary"],
    # "hungary": ["hungary", "budapest", "debrecen", "szeged", "eger"],
    # "poland": ["poland", "warsaw", "krakow", "gdansk", "wroclaw", "poznan", "zakopane"],
    # "croatia": ["croatia", "zagreb", "dubrovnik", "split", "zadar", "hvar", "korcula", "plivicenationalpark"],
    # "turkey": ["turkey", "istanbul", "antalya", "cappadocia", "bodrum", "ankara", "izmir", "pamukkale"],
    # "norway": ["norway", "oslo", "bergen", "tromso", "alesund", "stavanger", "lofoten"],
    # "sweden": ["sweden", "stockholm", "gothenburg", "malmo", "uppsala"],
    # "denmark": ["denmark", "copenhagen", "aarhus", "odense"],
    # "finland": ["finland", "helsinki", "rovaniemi", "turku"],
    # "iceland": ["iceland", "reykjavik", "akureyri", "goldencircle", "bluelagoon"],
    # "ireland": ["ireland", "dublin", "galway", "cork", "limerick", "kilkenny", "kerry"],
    # "scotland": ["scotland", "edinburgh", "glasgow", "inverness", "isleofskye"],
    # "russia": ["russia", "moscow", "saintpetersburg", "kazan", "sochi", "vladivostok"],
    # "ukraine": ["ukraine", "kyiv", "lviv", "odessa", "kharkiv"],
    # "romania": ["romania", "bucharest", "brasov", "sibiu", "clujnapoca"],
    # "bulgaria": ["bulgaria", "sofia", "plovdiv", "varna"],
    # "slovakia": ["slovakia", "bratislava", "kosice"],
    # "slovenia": ["slovenia", "ljubljana", "bled"],
    # "estonia": ["estonia", "tallinn", "tartu"],
    # "latvia": ["latvia", "riga"],
    # "lithuania": ["lithuania", "vilnius", "kaunas"],
    # "albania": ["albania", "tirana", "sarande"],
    # "montenegro": ["montenegro", "kotor", "budva", "podgorica"],
    # "serbia": ["serbia", "belgrade", "novisad"],
    # "bosnia": ["bosnia", "sarajevo", "mostar"],
    # "northmacedonia": ["northmacedonia", "skopje", "ohrid"],
    # "luxembourg": ["luxembourg"],
    # "malta": ["malta", "valletta", "gozo", "mdina"],

    # East Asia
    # "china": ["china", "beijing", "shanghai", "xian", "chengdu", "guangzhou", "shenzhen", "hangzhou", "suzhou", "zhangjiajie", "guilin", "yangshuo", "lijiang", "kunming", "hongkong", "macau", "tibet", "harbin"],
    # "japan": ["japan", "tokyo", "kyoto", "osaka", "hiroshima", "nagasaki", "fukuoka", "sapporo", "okinawa", "hakone", "nara", "mtfuji", "kanazawa", "takayama"],
    # "korea": ["korea", "seoul", "busan", "jeju", "incheon", "daegu", "gwangju", "suwon", "gangneung", "andong"],
    # "taiwan": ["taiwan", "taipei", "kaohsiung", "taichung", "tainan", "hualien", "tarokogorge", "sunmoonlake", "alishan", "keelung"],
    # "mongolia": ["mongolia", "ulanbator", "gobidesert", "karakorum", "tereljnationalpark", "khustainuruu"],
    
    #The Americas: 
    # "california": ["california", "losangeles", "sanfrancisco", "sandiego", "yosemite", "deathvalley", "napa", "santamonica", "hollywood", "laketahoe"],
    # "nyc": ["newyork", "newyorkcity", "brooklyn", "manhattan", "niagarafalls"],
    # "florida": ["florida", "miami", "orlando", "tampa", "keywest", "everglades"],
    # "arizona": ["arizona", "grandcanyon", "phoenix", "sedona", "antelopecanyon", "monumentvalley"],
    # "texas": ["texas", "austin", "houston", "dallas", "sanantonio", "fortworth"],
    # "washington": ["washington", "seattle", "olympicnationalpark", "mountsthelens", "spokane"],
    # "nevada": ["nevada", "lasvegas", "renonv", "laketahoe"],
    # "colorado": ["colorado", "denver", "rockymountains", "coloradosprings"],
    # "hawaii": ["hawaii", "honolulu", "maui", "bigisland", "kauai"],
    # "alaska": ["alaska", "anchorage", "denalinationalpark", "juneau"],
    # "maine": ["maine", "portlandmaine", "acadianationalpark"],
    # "utah": ["utah", "zionnationalpark", "brycecanyon", "saltlakecity"],
    # "massachusetts": ["massachusetts", "boston", "capecod"],
    # "oregon": ["oregon", "portlandoregon", "craterlake", "bendoregon"],

    # "canada": ["canada", "toronto", "vancouver", "montreal", "quebeccity", "banff", "calgary", "niagarafalls", "ottawa", "victoria", "whistler"],
    # "mexico": ["mexico", "mexicocity", "cancun", "tulum", "playadelcarmen", "puertovallarta", "guadalajara", "loscabos", "oaxaca", "merida", "cozumel"],
    # "guatemala": ["guatemala", "antigua", "lagoatitlan", "tikal"],
    # "costarica": ["costarica", "sanjose", "monteverde", "arenal", "manuelantonio", "tamarindo"],
    # "panama": ["panama", "panamacity", "bocasdeltoro", "boquete", "sanblas"],
    # "belize": ["belize", "belizecity", "ambergris", "caye", "cayecaulker", "belmopan"],

    # South America
    # "brazil": ["brazil", "riodejaneiro", "saopaulo", "iguazu", "salvador", "manaus", "pantanal", "florianopolis"],
    # "argentina": ["argentina", "buenosaires", "patagonia", "iguazufalls", "bariloche", "ushuaia", "mendoza", "salta"],
    # "peru": ["peru", "lima", "cusco", "machupicchu", "sacredvalley", "arequipa", "lakeniticaca"],
    # "colombia": ["colombia", "cartagena", "medellin", "bogota", "salento", "tayrona"],
    # "chile": ["chile", "santiago", "patagonia", "valparaiso", "easterisland", "atacamadesert"],
    # "ecuador": ["ecuador", "quito", "galapagos", "guayaquil", "banos", "cuenca"],
    # "bolivia": ["bolivia", "lapaz", "uyunisaltflats", "sucre", "copacabana"],

    # #Africa
    # "southafrica": ["southafrica", "capetown", "johannesburg", "durban", "krugernationalpark", "gardenroute", "stellenbosch"],
    # "morocco": ["morocco", "marrakech", "casablanca", "fes", "chefchaouen", "merzouga", "tangier", "essaouira"],
    # "tunisia": ["tunisia", "tunis", "sousse", "monastir", "dougga", "tozeur", "djerba"],
    # "egypt": ["egypt", "cairo", "alexandria", "giza", "luxor", "aswan", "hurghada", "sharmelsheikh", "siwa"],
    # "ghana": ["ghana", "accra"],
    # "nigeria": ["nigeria", "lagos", "abuja", "calabar", "lekki", "kano"],
    # "zimbabwe": ["zimbabwe", "victoriafalls"],
    # "tanzania": ["tanzania", "zanzibar", "kilimanjaro", "serengeti", "ngorongoro", "daressalaam", "arusha"],
    # "kenya": ["kenya", "nairobi", "masaimara", "mombasa", "lakenakuru"],
    # "namibia": ["namibia", "windhoek", "sossusvlei", "etosha", "swakopmund", "skeletoncoast"],
    # "botswana": ["botswana"],
    # "ethiopia": ["ethiopia", "addisababa"],

    #Central Asia
    # "kazakhstan": ["kazakhstan", "almaty", "astana", "shymkent", "charyn"],
    # "uzbekistan": ["uzbekistan", "samarkand", "bukhara", "khiva", "tashkent"],
    # "kyrgyzstan": ["kyrgyzstan", "bishkek", "karakol", "issyk", "osh"],

    # #Oceania
    # "australia": ["australia", "sydney", "melbourne", "brisbane", "perth", "adelaide", "goldcoast", "uluru", "tasmania", "greatbarrierreef"],
    # "new_zealand": ["newzealand", "auckland", "queenstown"],

    # #Middle East
    # "saudi_arabia": ["saudiarabia", "riyadh", "jeddah", "mecca"],
    # "qatar": ["qatar", "doha"],
    # "uae": ["uae", "dubai", "abudhabi", "sharjah"],
    # "jordan": ["jordan", "amman", "petra", "wadirum", "deadsea", "aqaba"],
    # "israel": ["israel", "jerusalem", "telaviv"],

    # #South Asia
    # "india": ["india", "delhi", "mumbai", "jaipur", "agra", "kerala", "varanasi", "goa", "ladakh", "kashmir", "kolkata", "hyderabad"],
    # "pakistan": ["pakistan", "lahore", "karachi", "islamabad", "gilgit", "hunza", "swatvalley", "quetta"],
    # "bangladesh": ["bangladesh", "dhaka", "chittagong", "sylhet", "coxsbazar", "sundarbans"],
    # "sri_lanka": ["srilanka", "colombo", "kandy", "ella", "sigiriya", "galle", "nuwaraeliya"],
    # "nepal": ["nepal", "kathmandu", "pokhara", "lukla", "everestbasecamp", "bhaktapur", "chitwannationalpark"],    
}

client = OpenAI(
    project='proj_Ae4DRM4LfOvsBwmuXUvqZwPr',
    api_key=os.environ.get("OPENAI_API_KEY"),
)

app = Flask(__name__, static_folder="static")
app.secret_key = os.urandom(24)  
CORS(app, resources={r"/search": {"origins": "*"}})

limiter = Limiter(key_func=get_remote_address)
limiter.init_app(app)

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
                        add_limited_posts(filtered_posts, 4)
                        break  # Stop after finding first valid subreddit
                except requests.exceptions.RequestException:
                    pass
    except requests.exceptions.RequestException:
        pass

    # 2. Check country/region subreddit (max 3 posts)
    query_lower = query.lower()
    for country, locations in LOCATION_MAPPINGS.items():
        # Check if any part of the query matches a location
        if any(location in query_lower for location in locations) or query_lower == country:
            country_subreddit = locations[0]
        # Use the actual matched location for searching
            matched_location = next((loc for loc in locations if loc in query_lower), query_lower)
            search_url = f"https://www.reddit.com/r/{country_subreddit}/search.json?q={quote(matched_location)}&restrict_sr=1&limit=100&sort=top"
            try:
                response = requests.get(search_url, headers=google_headers)
                if response.status_code == 200:
                    data = response.json()
                    posts = [post["data"] for post in data.get("data", {}).get("children", [])]
                    print(f"Found {len(posts)} basic posts in r/{country_subreddit}") 
                    filtered_posts = filter_posts(posts, is_location_specific_subreddit=False)
                    print(f"Found {len(filtered_posts)} matching posts in r/{country_subreddit}")  # Debug print
                    add_limited_posts(filtered_posts, 3)
            except requests.exceptions.RequestException:
                pass

    # 3. Check general travel subreddits for remaining slots
    general_subreddits = ["travel", "solotravel", "travelnopics"]
    posts_needed = 12 - len(all_posts)
    if posts_needed > 0:
        posts_per_subreddit = max(1, posts_needed // len(general_subreddits))
        for subreddit in general_subreddits:
            if len(all_posts) >= 12:
                break
            search_url = f"https://www.reddit.com/r/{subreddit}/search.json?q={quote(query)}&restrict_sr=1&limit=100&sort=top"
            try:
                response = requests.get(search_url, headers=google_headers)
                if response.status_code == 200:
                    data = response.json()
                    posts = [post["data"] for post in data.get("data", {}).get("children", [])]
                    filtered_posts = filter_posts(posts, is_location_specific_subreddit=False)
                    remaining_slots = min(posts_per_subreddit, 12 - len(all_posts))
                    add_limited_posts(filtered_posts, remaining_slots)
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

        session["cached_posts"] = posts
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



@app.route("/generate_itinerary", methods=["POST"])
def generate_itinerary():
    try:
        data = request.get_json()
        query = data.get("location", "").strip()
        days = data.get("days", 1)

        if not query or not days:
            return jsonify({"error": "Location and number of days are required."}), 400

        cached_query = session.get("cached_query")
        cached_posts = session.get("cached_posts")
        if cached_query == query and cached_posts:
            posts = cached_posts
        else:
            posts = fetch_reddit_posts(query, "travel")


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
            session["cached_posts"] = posts


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
            " For each day, recommend specific activities, locations, or experiences based on the posts and comments details only. If there is limited info, feel free to supplement with logical suggestions."
            " Keep the language simple, avoid overly large or convoluted words, and spread activities logically across all days where possible."
            " Format the itinerary clearly with line breaks and bullet points. Do a line break after EVERY day of the itinerary generated. For example:"
            "'Day 1:' followed by a line break, then use '- Activity 1', line break, '- Activity 2', and so on for each day. Repeat this format for subsequent days."
            " Start by saying '<n>-day itinerary in <location>', and do NOT add a summary of the area or how to get there (e.g., from the airport)."
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
