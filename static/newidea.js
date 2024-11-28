document.addEventListener("DOMContentLoaded", () => {
  const searchButton = document.getElementById("search-button");
  const foodButton = document.getElementById("food-button");
  const budgetButton = document.getElementById("budget-button");
  const itineraryButton = document.getElementById("itinerary-button");
  const locationInput = document.getElementById("location-input");
  const daysInput = document.getElementById("days-input");
  const resultsDiv = document.getElementById("results");
  const body = document.body;

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
            ? `${postText.slice(
                0,
                500
              )}<span style="color: blue; cursor: pointer;" class="show-more-post">... [show more]</span>`
            : postText;

        postTextDiv.innerHTML = truncatedPostText;

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
        commentsDiv.innerHTML = comments
          .map((comment) => `<p>${comment}</p>`)
          .join("");

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
    if (!location) {
      resultsDiv.innerHTML = "<p>Please enter a location.</p>";
      return;
    }

    resultsDiv.innerHTML = "<p>Loading...</p>";
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
    if (!location || !days) {
      resultsDiv.innerHTML =
        "<p>Please enter both a location and number of days.</p>";
      return;
    }

    resultsDiv.innerHTML = "<p>Loading itinerary...</p>";

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
