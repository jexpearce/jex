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
      // Send request to Flask backend
      const response = await fetch(
        `http://127.0.0.1:5000/search?q=${location}&subreddit=travel`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const posts = data.data.children;

      if (posts.length === 0) {
        resultsDiv.innerHTML = "<p>No results found.</p>";
      } else {
        // Define keywords for filtering
        const keywords = ["itinerary", "guide", "things to do", "tips"];
        const keywordRegex = new RegExp(keywords.join("|"), "i");

        const filteredPosts = posts
          .map((post) => post.data)
          .filter((post) => keywordRegex.test(post.title)) // Match keywords
          .sort((a, b) => b.ups - a.ups) // Sort by upvotes
          .slice(0, 10); // Top 10

        if (filteredPosts.length === 0) {
          resultsDiv.innerHTML = "<p>No posts matched your keywords.</p>";
        } else {
          resultsDiv.innerHTML = "<h2>Top Posts:</h2><ul>";
          filteredPosts.forEach((post) => {
            const title = post.title;
            const postUrl = `https://reddit.com${post.permalink}`;
            const upvotes = post.ups;

            resultsDiv.innerHTML += `<li><a href="${postUrl}" target="_blank">${title}</a> (${upvotes} upvotes)</li>`;
          });
          resultsDiv.innerHTML += "</ul>";
        }
      }
    } catch (error) {
      console.error(error);
      resultsDiv.innerHTML = `<p>Failed to fetch data: ${error.message}</p>`;
    }
  });
});
