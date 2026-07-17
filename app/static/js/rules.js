// Rules page - fetches and renders the rules list.
document.addEventListener("DOMContentLoaded", async () => {
  const list = document.getElementById("rules-list");

  try {
    const res = await fetch("/api/rules");
    if (!res.ok) throw new Error("Request failed");
    const data = await res.json();

    list.innerHTML = "";
    data.rules.forEach((rule) => {
      const li = document.createElement("li");
      li.className = "rule-item";
      li.textContent = rule.text;
      list.appendChild(li);
    });
  } catch (err) {
    list.innerHTML = '<li class="rule-item">Couldn\'t load rules. Try refreshing.</li>';
  }
});
