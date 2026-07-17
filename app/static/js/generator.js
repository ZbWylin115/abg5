// Generator page logic — fetches a placeholder entry from the API.
document.addEventListener("DOMContentLoaded", () => {
  const outputBox = document.getElementById("output-box");
  const generateBtn = document.getElementById("generate-btn");

  async function fetchRandomEntry() {
    outputBox.classList.add("loading");
    try {
      const res = await fetch("/api/generator/random");
      if (!res.ok) throw new Error("Request failed");
      const data = await res.json();
      outputBox.textContent = data.entry;
    } catch (err) {
      outputBox.textContent = "Couldn't reach the generator. Try again.";
    } finally {
      outputBox.classList.remove("loading");
    }
  }

  generateBtn.addEventListener("click", fetchRandomEntry);

  // Load one entry on page load so the panel isn't empty.
  fetchRandomEntry();
});
