document.addEventListener("DOMContentLoaded", () => {
  const searchButton = document.getElementById("search-button");
  const locationInput = document.getElementById("location-input");
  const resultsDiv = document.getElementById("results");

  searchButton.addEventListener("click", async () => {
    const location = locationInput.value.trim();
    if (!location) {
      resultsDiv.innerHTML = "<p>Please enter a location.</p>";
      return;
    }

    resultsDiv.innerHTML = "<p>Loading...</p>";

    try {
      const response = await fetch(
        `http://127.0.0.1:5001/search?q=${encodeURIComponent(location)}`
      );
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

          // Add "Show Post" button
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

            // Toggle post text visibility
            showPostBtn.addEventListener("click", () => {
              if (postTextDiv.style.display === "none") {
                postTextDiv.style.display = "block";
                showPostBtn.textContent = "Hide Post";
              } else {
                postTextDiv.style.display = "none";
                showPostBtn.textContent = "Show Post";
              }
            });

            // Add "Show More" and "Show Less" functionality
            postTextDiv.addEventListener("click", (event) => {
              const target = event.target;
              if (target.classList.contains("show-more-post")) {
                postTextDiv.innerHTML = `${postText} <span style="color: blue; cursor: pointer;" class="show-less-post">[show less]</span>`;
              } else if (target.classList.contains("show-less-post")) {
                postTextDiv.innerHTML = truncatedPostText;
              }
            });

            postItem.appendChild(showPostBtn);
            postItem.appendChild(postTextDiv);
          }

          // Add "Show Comments" button and truncated comments
          if (comments.length > 0) {
            const commentsBtn = document.createElement("button");
            commentsBtn.textContent = "Show Comments";
            commentsBtn.className = "show-comments-btn";

            const commentsDiv = document.createElement("div");
            commentsDiv.style.display = "none";
            commentsDiv.innerHTML = comments
              .map((comment, index) =>
                comment.length > 500
                  ? `<p>${comment.slice(
                      0,
                      500
                    )}<span style="color: blue; cursor: pointer;" class="show-more-comment" data-index="${index}">... [show more]</span></p>`
                  : `<p>${comment}</p>`
              )
              .join("");

            // Expand/collapse comment text
            commentsDiv.addEventListener("click", (event) => {
              const target = event.target;
              if (target.classList.contains("show-more-comment")) {
                const index = target.dataset.index;
                target.parentNode.innerHTML = `${comments[index]} <span style="color: blue; cursor: pointer;" class="show-less-comment" data-index="${index}">[show less]</span>`;
              } else if (target.classList.contains("show-less-comment")) {
                const index = target.dataset.index;
                target.parentNode.innerHTML = `${comments[index].slice(
                  0,
                  500
                )}<span style="color: blue; cursor: pointer;" class="show-more-comment" data-index="${index}">... [show more]</span>`;
              }
            });

            // Toggle comments visibility
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
  });
});
