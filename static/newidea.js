const cities = [
  "Abu Dhabi",
  "Agra",
  "Amalfi",
  "Amsterdam",
  "Angkor Wat",
  "Athens",
  "Auckland",
  "Bali",
  "Bangkok",
  "Barcelona",
  "Beijing",
  "Berlin",
  "Bogota",
  "Bordeaux",
  "Boston",
  "Brisbane",
  "Brighton",
  "Bristol",
  "Glasgow",
  "Brussels",
  "Budapest",
  "Buenos Aires",
  "Cairo",
  "Cancun",
  "Cape Town",
  "Cappadocia",
  "Cartagena",
  "Casablanca",
  "Chiang Mai",
  "Chicago",
  "Copenhagen",
  "Cusco",
  "Da Nang",
  "Delhi",
  "Denver",
  "Dubai",
  "Dublin",
  "Edinburgh",
  "Florence",
  "Frankfurt",
  "Fez",
  "Geneva",
  "Granada",
  "Grand Canyon",
  "Hanoi",
  "Havana",
  "Helsinki",
  "Ho Chi Minh",
  "Hong Kong",
  "Honolulu",
  "Istanbul",
  "Jakarta",
  "Jerusalem",
  "Johannesburg",
  "Kathmandu",
  "Krakow",
  "Kuala Lumpur",
  "Kyoto",
  "Las Vegas",
  "Lima",
  "Lisbon",
  "Liverpool",
  "London",
  "Los Angeles",
  "Luxembourg",
  "Lyon",
  "Macau",
  "Madrid",
  "Manchester",
  "Leeds",

  "Manila",
  "Marrakech",
  "Marseille",
  "Melbourne",
  "Mexico City",
  "Miami",
  "Milan",
  "Montreal",
  "Moscow",
  "Mumbai",
  "Munich",
  "Nairobi",
  "Naples",
  "Nashville",
  "New Orleans",
  "New York",
  "Nice",
  "Osaka",
  "Oslo",
  "Oxford",
  "Palermo",
  "Paris",
  "Perth",
  "Petra",
  "Phuket",
  "Porto",
  "Prague",
  "Quebec",
  "Queenstown",
  "Quito",
  "Reykjavik",
  "Rio",
  "Rome",
  "Rotterdam",
  "Lake Tahoe",
  "Nouakchott",
  "England",

  "Saint Petersburg",
  "Salt Lake City",
  "Salvador",
  "San Diego",
  "San Francisco",
  "San Juan",
  "San Sebastian",
  "Santiago",
  "Sao Paulo",
  "Seattle",
  "Seoul",
  "Seville",
  "Shanghai",
  "Sicily",
  "Singapore",
  "Stockholm",
  "Sydney",
  "Taipei",
  "Tallinn",
  "Tel Aviv",
  "Tokyo",
  "Toronto",
  "Tuscany",
  "Valencia",
  "Vancouver",
  "Vang Vieng",
  "Vientiane",
  "Venice",
  "Vienna",
  "Warsaw",
  "Washington DC",
  "Wellington",
  "Yangon",
  "Yellowstone",
  "York",
  "Zagreb",
  "Zanzibar",
  "Zurich",
  // More specific tourist destinations
  "Amalfi Coast",
  "Amazon Rainforest",
  "Great Barrier Reef",
  "Lake Como",
  "Niagara Falls",
  "Santorini",
  "Swiss Alps",
  // Beach destinations
  "Bora Bora",
  "Ibiza",
  "Maldives",
  "Maui",
  "Mykonos",
  "Seychelles",
  "Tahiti",
  "Acropolis",
  "Great Wall of China",
  "Machu Picchu",
  "Pompeii",
  "Stonehenge",
  "Taj Mahal",
  "Vatican City",
  "Antigua",
  "Arequipa",
  "Bratislava",
  "Bucharest",
  "Busan",
  "Cali",
  "Cebu",
  "Chiang Rai",
  "Da Lat",
  "Da Nang",
  "El Nido",
  "Florianópolis",
  "Goa",
  "Guadalajara",
  "Hoi An",
  "Huacachina",
  "Hua Hin",
  "Ilha Grande",
  "Koh Lanta",
  "Koh Phangan",
  "Koh Phi Phi",
  "Koh Tao",
  "Kotor",
  "Krabi",
  "Kuching",
  "La Paz",
  "Lake Atitlan",
  "Luang Prabang",
  "Medellin",
  "Mui Ne",
  "Nha Trang",
  "Pai",
  "Palawan",
  "Penang",
  "Phnom Penh",
  "Puerto Escondido",
  "Pushkar",
  "Rishikesh",
  "San Cristobal",
  "San Juan del Sur",
  "Sapa",
  "Siem Reap",
  "Siargao",
  "Sofia",
  "Split",
  "Sucre",
  "Tbilisi",
  "Varanasi",

  "Thailand",
  "Japan",
  "France",
  "Spain",
  "Italy",
  "Greece",
  "USA",
  "UK",
  "Australia",
  "Germany",
  "Indonesia",
  "Vietnam",
  "Mexico",
  "Turkey",
  "Portugal",
  "Switzerland",
  "Netherlands",
  "Morocco",
  "Canada",
  "Croatia",
  "Ireland",
  "Austria",
  "Egypt",
  "South Korea",
  "Singapore",
  "Czech Republic",
  "Hungary",
  "Poland",
  "Peru",
  "Philippines",
  "Norway",
  "Sweden",
  "Denmark",
  "Iceland",
  "Brazil",
  "Argentina",
  "Colombia",
  "Costa Rica",
  "Cambodia",
  "Malaysia",
  "India",
  "Nepal",
  "Sri Lanka",
  "Jordan",
  "Israel",
  "South Africa",
  "New Zealand",
  "Belgium",
  "Romania",
  "China",

  "Scotland",
  "Wales",
  "Malta",
  "Montenegro",
  "Albania",
  "Slovenia",
  "Slovakia",
  "Finland",
  "Estonia",
  "Latvia",
  "Lithuania",
  "Ukraine",
  "Georgia",
  "Armenia",
  "Bulgaria",
  "Serbia",
  "Bosnia",
  "Ecuador",
  "Chile",
  "Bolivia",
  "Guatemala",
  "Nicaragua",
  "Panama",
  "Cuba",
  "Jamaica",
  "Dominican Republic",
  "Bahamas",
  "Puerto Rico",
  "Maldives",
  "UAE",
  "Qatar",
  "Oman",
  "Lebanon",
  "Tunisia",
  "Kenya",
  "Tanzania",
  "Uganda",
  "Rwanda",
  "Madagascar",
  "Zimbabwe",
  "Namibia",
  "Botswana",
  "Myanmar",
  "Laos",
  "Taiwan",

  "Bhutan",
  "Mongolia",
  "Kazakhstan",
  "Uzbekistan",
  "Iran",
  "Azerbaijan",
  "North Macedonia",
  "Luxembourg",
  "Liechtenstein",
  "Andorra",
  "San Marino",
  "Cyprus",
  "Seychelles",
  "Mauritius",
  "Fiji",
  "Samoa",
  "Tonga",
  "Vanuatu",
  "Brunei",
  "Bangladesh",
  "Pakistan",
  "Ethiopia",
  "Ghana",
  "Senegal",
  "Cape Verde",
  "Morocco",
  "Paraguay",
  "Uruguay",
  "Venezuela",
  "Guyana",
  "Suriname",
  "El Salvador",
  "Honduras",
  "Belize",
  "Barbados",
];

// Add this at the top of newidea.js
const rateLimiter = {
  requests: {},
  timeWindow: 60000, // 1 minute
  maxRequests: 30, // Conservative limit

  canMakeRequest: function (location) {
    const now = Date.now();
    if (!this.requests[location]) {
      this.requests[location] = [now];
      return true;
    }

    // Clean old requests
    this.requests[location] = this.requests[location].filter(
      (time) => now - time < this.timeWindow
    );

    if (this.requests[location].length >= this.maxRequests) {
      return false;
    }

    this.requests[location].push(now);
    return true;
  },
};

let isLoading = false;

const setButtonsDisabled = (disabled) => {
  document.querySelectorAll("button").forEach((btn) => {
    btn.disabled = disabled;
  });
};

document.addEventListener("DOMContentLoaded", () => {
  const searchButton = document.getElementById("search-button");
  const foodButton = document.getElementById("food-button");
  const budgetButton = document.getElementById("budget-button");
  const itineraryButton = document.getElementById("itinerary-button");
  const locationInput = document.getElementById("location-input");
  const daysInput = document.getElementById("days-input");
  const resultsDiv = document.getElementById("results");
  const body = document.body;

  // NEW: Create wrapper and dropdown for autocomplete
  const inputWrapper = document.createElement("div");
  inputWrapper.className = "location-input-wrapper";
  locationInput.parentNode.insertBefore(inputWrapper, locationInput);
  inputWrapper.appendChild(locationInput);

  const dropdown = document.createElement("div");
  dropdown.className = "autocomplete-dropdown";
  inputWrapper.appendChild(dropdown);

  // NEW: Track selected item in dropdown
  let selectedIndex = -1;

  // NEW: Handle user typing in the location input
  locationInput.addEventListener("input", (e) => {
    const value = e.target.value.toLowerCase();
    if (!value) {
      dropdown.classList.remove("active");
      return;
    }

    // Filter cities based on input and show top 5 matches
    const filteredCities = cities
      .filter((city) => city.toLowerCase().includes(value))
      .slice(0, 5);

    if (filteredCities.length) {
      dropdown.innerHTML = filteredCities
        .map(
          (city, index) => `
          <div class="autocomplete-item ${
            index === selectedIndex ? "selected" : ""
          }" 
               data-value="${city}">
            ${city}
          </div>
        `
        )
        .join("");
      dropdown.classList.add("active");
    } else {
      dropdown.classList.remove("active");
    }
  });

  // NEW: Handle keyboard navigation in dropdown
  locationInput.addEventListener("keydown", (e) => {
    const items = dropdown.querySelectorAll(".autocomplete-item");

    if (e.key === "ArrowDown") {
      e.preventDefault();
      selectedIndex = Math.min(selectedIndex + 1, items.length - 1);
      updateSelection();
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      selectedIndex = Math.max(selectedIndex - 1, 0);
      updateSelection();
    } else if (e.key === "Enter" && selectedIndex >= 0) {
      e.preventDefault();
      const selected = items[selectedIndex];
      if (selected) {
        locationInput.value = selected.dataset.value;
        dropdown.classList.remove("active");
      }
    }
  });

  // NEW: Handle clicking on dropdown items
  dropdown.addEventListener("click", (e) => {
    const item = e.target.closest(".autocomplete-item");
    if (item) {
      locationInput.value = item.dataset.value;
      dropdown.classList.remove("active");
    }
  });

  // NEW: Close dropdown when clicking outside
  document.addEventListener("click", (e) => {
    if (!inputWrapper.contains(e.target)) {
      dropdown.classList.remove("active");
      selectedIndex = -1;
    }
  });

  // NEW: Helper function to update selected item styling
  function updateSelection() {
    const items = dropdown.querySelectorAll(".autocomplete-item");
    items.forEach((item, index) => {
      item.classList.toggle("selected", index === selectedIndex);
      if (index === selectedIndex) {
        item.scrollIntoView({ block: "nearest" });
      }
    });
  }

  const renderPosts = (posts) => {
    const postList = document.getElementById("post-list");
    postList.innerHTML = "";

    posts.forEach((post) => {
      const title = post.title;
      const postUrl = `https://reddit.com${post.permalink}`;
      const upvotes = post.ups;
      const postText = post.selftext || "";
      const comments = (post.top_comments || []).filter(
        (comment) =>
          comment &&
          comment.trim() !== "[deleted]" &&
          comment.trim() !== "[removed]"
      );

      const postItem = document.createElement("li");
      postItem.innerHTML = `
          <a href="${postUrl}" target="_blank">${title}</a> (${upvotes} upvotes)
        `;

      if (postText) {
        const showPostBtn = document.createElement("button");
        showPostBtn.textContent = "Show Post";
        showPostBtn.className = "show-post-btn";

        const postTextDiv = document.createElement("div");
        postTextDiv.style.display = "none";

        const truncatedPostText =
          postText.length > 500
            ? `<div class="truncated-content">
             ${postText.slice(0, 500)}
             <span class="show-more">[show more]</span>
             <div class="full-text" style="display: none;">
               ${postText.slice(500)}
               <span class="show-less">[show less]</span>
             </div>
           </div>`
            : postText;

        postTextDiv.innerHTML = truncatedPostText;

        // Update the click handler
        const showMoreSpan = postTextDiv.querySelector(".show-more");
        const showLessSpan = postTextDiv.querySelector(".show-less");
        const fullText = postTextDiv.querySelector(".full-text");

        if (showMoreSpan) {
          showMoreSpan.addEventListener("click", () => {
            showMoreSpan.style.display = "none";
            fullText.style.display = "inline";
          });
        }

        if (showLessSpan) {
          showLessSpan.addEventListener("click", () => {
            fullText.style.display = "none";
            showMoreSpan.style.display = "inline";
          });
        }

        showPostBtn.addEventListener("click", () => {
          if (postTextDiv.style.display === "none") {
            postTextDiv.style.display = "block";
            showPostBtn.textContent = "Hide Post";
          } else {
            postTextDiv.style.display = "none";
            showPostBtn.textContent = "Show Post";
          }
        });

        postItem.appendChild(showPostBtn);
        postItem.appendChild(postTextDiv);
      }

      if (comments.length > 0) {
        const commentsBtn = document.createElement("button");
        commentsBtn.textContent = "Show Comments";
        commentsBtn.className = "show-comments-btn";

        const commentsDiv = document.createElement("div");
        commentsDiv.style.display = "none";
        comments.forEach((comment) => {
          const commentDiv = document.createElement("div");
          commentDiv.className = "comment";

          if (comment.length > 200) {
            const truncatedComment = `
              <div class="truncated-content">
                ${comment.slice(0, 200)}
                <span class="show-more">[show more]</span>
                <div class="full-text" style="display: none;">
                  ${comment.slice(200)}
                  <span class="show-less">[show less]</span>
                </div>
              </div>
            `;
            commentDiv.innerHTML = truncatedComment;

            const showMore = commentDiv.querySelector(".show-more");
            const showLess = commentDiv.querySelector(".show-less");
            const fullText = commentDiv.querySelector(".full-text");

            showMore.addEventListener("click", () => {
              fullText.style.display = "inline";
              showMore.style.display = "none";
            });

            showLess.addEventListener("click", () => {
              fullText.style.display = "none";
              showMore.style.display = "inline";
            });
          } else {
            commentDiv.textContent = comment;
          }

          commentsDiv.appendChild(commentDiv);
        });
        commentsBtn.addEventListener("click", () => {
          if (commentsDiv.style.display === "none") {
            commentsDiv.style.display = "block";
            commentsBtn.textContent = "Hide Comments";
          } else {
            commentsDiv.style.display = "none";
            commentsBtn.textContent = "Show Comments";
          }
        });

        postItem.appendChild(commentsBtn);
        postItem.appendChild(commentsDiv);
      }

      postList.appendChild(postItem);
    });
  };

  const performSearch = async (location, type) => {
    location = location.trim();
    if (!location || location.length < 2) {
      resultsDiv.innerHTML = "<p>Please enter a valid location name</p>";
      return;
    }

    if (!rateLimiter.canMakeRequest(location)) {
      resultsDiv.innerHTML =
        "<p>Too many requests. Please wait a minute and try again.</p>";
      return;
    }
    if (!location) {
      resultsDiv.innerHTML = "<p>Please enter a location.</p>";
      return;
    }
    resultsDiv.innerHTML = `
      <div class="loading-indicator">
        <i class="fas fa-spinner"></i>
        <span>Finding the best ${type} tips...</span>
      </div>
    `;
    body.classList.add("results-shown");

    try {
      const endpoint =
        type === "food"
          ? `/search?type=food&q=${encodeURIComponent(location)}`
          : type === "budget"
          ? `/search?type=budget&q=${encodeURIComponent(location)}`
          : `/search?q=${encodeURIComponent(location)}`;
      const response = await fetch(endpoint);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const posts = await response.json();

      if (posts.length === 0) {
        resultsDiv.innerHTML = "<p>No results found.</p>";
      } else {
        resultsDiv.innerHTML = `
          <h2 style="color: white;">Top Posts:</h2>
          <button id="generate-summary">Generate Summary</button>
          <div id="summary-output"></div>
          <ul id='post-list'></ul>
        `;
        const generateSummaryButton =
          document.getElementById("generate-summary");

        renderPosts(posts);

        generateSummaryButton.addEventListener("click", async () => {
          try {
            generateSummaryButton.remove();
            const summaryOutput = document.getElementById("summary-output");
            summaryOutput.innerText = "Generating summary...";

            const response = await fetch("/summarize", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ posts, type }),
            });

            if (!response.ok) {
              throw new Error(`Failed to summarize: ${response.statusText}`);
            }

            const { summary } = await response.json();
            summaryOutput.innerText = summary;
          } catch (error) {
            console.error(error);
            const summaryOutput = document.getElementById("summary-output");
            summaryOutput.innerText = "Failed to generate summary.";
          }
        });
      }
    } catch (error) {
      console.error(error);
      resultsDiv.innerHTML = `<p style="color: white;">Failed to fetch data: ${error.message}</p>`;
    }
  };

  const generateItinerary = async (location, days) => {
    location = location.trim();
    days = parseInt(days);

    if (!location || location.length < 2) {
      resultsDiv.innerHTML = "<p>Please enter a valid location name.</p>";
      return;
    }

    if (isNaN(days) || days < 1 || days > 20) {
      resultsDiv.innerHTML =
        "<p>Please enter a number of days between 1 and 20.</p>";
      return;
    }

    if (!rateLimiter.canMakeRequest(location)) {
      resultsDiv.innerHTML =
        "<p>Too many requests. Please wait a minute and try again.</p>";
      return;
    }
    if (!location || !days) {
      resultsDiv.innerHTML =
        "<p>Please enter both a location and number of days.</p>";
      return;
    }

    resultsDiv.innerHTML = `
    <div class="loading-indicator">
      <i class="fas fa-spinner"></i>
      <span>Generating your perfect itinerary...</span>
    </div>
  `;

    try {
      const response = await fetch("/generate_itinerary", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ location, days }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const { itinerary, posts } = await response.json();

      resultsDiv.innerHTML = `
        <h2 style="color: white;">Your ${days}-Day Itinerary:</h2>
        <div id="itinerary-output">${itinerary}</div>
        <h2 style="color: white;">Top Posts:</h2>
        <ul id='post-list'></ul>
      `;

      renderPosts(posts);
    } catch (error) {
      console.error(error);
      resultsDiv.innerHTML = `<p style="color: white;">Failed to generate itinerary: ${error.message}</p>`;
    }
  };

  const handleSearch = (type) => {
    const location = locationInput.value.trim();
    performSearch(location, type);
  };

  const handleItinerary = () => {
    const location = locationInput.value.trim();
    const days = parseInt(daysInput.value.trim(), 10);
    generateItinerary(location, days);
  };

  searchButton.addEventListener("click", () => {
    handleSearch("travel");
  });

  foodButton.addEventListener("click", () => {
    handleSearch("food");
  });

  budgetButton.addEventListener("click", () => {
    handleSearch("budget");
  });

  itineraryButton.addEventListener("click", handleItinerary);
});
