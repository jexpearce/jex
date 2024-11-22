document.addEventListener("DOMContentLoaded", () => {
  const searchButton = document.getElementById("search-button");
  const foodButton = document.getElementById("food-button");
  const budgetButton = document.getElementById("budget-button");
  const locationInput = document.getElementById("location-input");
  const resultsDiv = document.getElementById("results");
  const body = document.getElementById("body");

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
        resultsDiv.innerHTML = "<h2>Top Posts:</h2><ul id='post-list'></ul>";
        const postList = document.getElementById("post-list");

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
              <a href="${postUrl}" target="_blank" style="font-size: 1.2em; font-weight: bold; text-decoration: none; color: #333;">
                ${title}
              </a> (${upvotes} upvotes)
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
      }
    } catch (error) {
      console.error(error);
      resultsDiv.innerHTML = `<p>Failed to fetch data: ${error.message}</p>`;
    }
  };

  searchButton.addEventListener("click", () => {
    const location = locationInput.value.trim();
    performSearch(location, "travel");
  });

  foodButton.addEventListener("click", () => {
    const location = locationInput.value.trim();
    performSearch(location, "food");
  });

  budgetButton.addEventListener("click", () => {
    const location = locationInput.value.trim();
    performSearch(location, "budget");
  });
});
