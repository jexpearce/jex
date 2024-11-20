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
          const title = post.title.replace(/\[.*?\]/g, "").trim(); // Remove [tags]
          const postUrl = `https://reddit.com${post.permalink}`;
          const upvotes = post.ups;

          // Check for post description
          const hasPostText = post.selftext && post.selftext.trim().length > 0;
          const postText =
            hasPostText && post.selftext.length > 300
              ? `${post.selftext.slice(0, 300)}... [click on post to see more]`
              : post.selftext;

          const comments = (post.top_comments || []).filter(
            (comment) =>
              comment && comment.trim() !== "[deleted]" && comment.length <= 500
          );

          const postItem = document.createElement("li");
          postItem.innerHTML = `
              <a href="${postUrl}" target="_blank">${title}</a>
              <span>(${upvotes} upvotes)</span>
            `;

          // Show Post Button (only if there is text)
          if (hasPostText) {
            const postBtn = document.createElement("button");
            postBtn.textContent = "Show Post";
            postBtn.className = "show-post-btn";

            const postDiv = document.createElement("div");
            postDiv.style.display = "none";
            postDiv.innerHTML = `<p>${postText}</p>`;

            postBtn.addEventListener("click", () => {
              if (postDiv.style.display === "none") {
                postDiv.style.display = "block";
                postBtn.textContent = "Hide Post";
              } else {
                postDiv.style.display = "none";
                postBtn.textContent = "Show Post";
              }
            });

            postItem.appendChild(postBtn);
            postItem.appendChild(postDiv);
          }

          // Show Comments Button (only if there are comments)
          if (comments.length > 0) {
            const commentsBtn = document.createElement("button");
            commentsBtn.textContent = "Show Comments";
            commentsBtn.className = "show-comments-btn";

            const commentsDiv = document.createElement("div");
            commentsDiv.style.display = "none";
            commentsDiv.innerHTML = comments
              .map((comment) => `<p>${comment}</p>`)
              .join("<br />");

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
