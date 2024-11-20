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
      // CORS Proxy URL
      const proxy = "https://cors-anywhere.herokuapp.com/";
      const url = `${proxy}https://www.reddit.com/r/travel/search.json?q=${location}&restrict_sr=1`;

      const response = await fetch(url);
      const data = await response.json();

      const posts = data.data.children;

      if (posts.length === 0) {
        resultsDiv.innerHTML = "<p>No results found.</p>";
      } else {
        // Define the keywords to match (case-insensitive)
        const keywords = ["itinerary", "guide", "things to do", "tips"];
        const keywordRegex = new RegExp(keywords.join("|"), "i");

        // Filter and sort posts
        const filteredPosts = posts
          .map((post) => post.data)
          .filter((post) => keywordRegex.test(post.title)) // Include only posts with matching keywords
          .sort((a, b) => b.ups - a.ups) // Sort by upvotes
          .slice(0, 10); // Take the top 10

        // Display results
        if (filteredPosts.length === 0) {
          resultsDiv.innerHTML = "<p>No posts matched your keywords.</p>";
        } else {
          resultsDiv.innerHTML = "<h2>Top Posts:</h2><ul>";
          filteredPosts.forEach((post) => {
            const title = post.title;
            const url = `https://reddit.com${post.permalink}`;
            const upvotes = post.ups;

            resultsDiv.innerHTML += `<li><a href="${url}" target="_blank">${title}</a> (${upvotes} upvotes)</li>`;
          });
          resultsDiv.innerHTML += "</ul>";
        }
      }
    } catch (error) {
      console.error(error);
      resultsDiv.innerHTML =
        "<p>Failed to fetch data. Please try again later.</p>";
    }
  });
});
