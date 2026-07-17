// Generator page logic - loads dropdown options from the API, sends
// user selections to /api/generate, and renders the results.

document.addEventListener("DOMContentLoaded", async () => {
  const archetypeContainer = document.getElementById("archetype-checkboxes");
  const citySelect = document.getElementById("city-select");
  const venueSelect = document.getElementById("venue-select");
  const interestSelect = document.getElementById("interest-select");
  const boldnessSelect = document.getElementById("boldness-select");
  const culturalToggle = document.getElementById("cultural-toggle");
  const cultureSelectWrapper = document.getElementById("culture-select-wrapper");
  const cultureSelect = document.getElementById("culture-select");
  const generateBtn = document.getElementById("generate-btn");
  const resultsPanel = document.getElementById("results-panel");

  function populateSelect(select, items, valueKey, labelKey, placeholder) {
    select.innerHTML = "";
    const opt = document.createElement("option");
    opt.value = "";
    opt.textContent = placeholder;
    select.appendChild(opt);
    items.forEach((item) => {
      const o = document.createElement("option");
      o.value = item[valueKey];
      o.textContent = item[labelKey];
      select.appendChild(o);
    });
  }

  function renderArchetypeCheckboxes(archetypes) {
    archetypeContainer.innerHTML = "";
    archetypes.forEach((a) => {
      const label = document.createElement("label");
      label.className = "checkbox-pill";

      const input = document.createElement("input");
      input.type = "checkbox";
      input.value = a.id;
      input.name = "archetype";

      input.addEventListener("change", () => {
        const checked = archetypeContainer.querySelectorAll("input:checked");
        if (checked.length > 2) {
          input.checked = false;
        }
      });

      label.appendChild(input);
      label.appendChild(document.createTextNode(a.name));
      archetypeContainer.appendChild(label);
    });
  }

  async function loadOptions() {
    const [archetypesRes, citiesRes, venuesRes, interestRes, boldnessRes, culturesRes] =
      await Promise.all([
        fetch("/api/archetypes").then((r) => r.json()),
        fetch("/api/cities").then((r) => r.json()),
        fetch("/api/venues").then((r) => r.json()),
        fetch("/api/interest-levels").then((r) => r.json()),
        fetch("/api/boldness-levels").then((r) => r.json()),
        fetch("/api/cultures").then((r) => r.json()),
      ]);

    renderArchetypeCheckboxes(archetypesRes.archetypes);
    populateSelect(citySelect, citiesRes.cities, "id", "name", "Any city");
    populateSelect(venueSelect, venuesRes.venues, "id", "name", "Any venue");
    populateSelect(interestSelect, interestRes.interest_levels, "id", "name", "Any interest level");
    populateSelect(boldnessSelect, boldnessRes.boldness_levels, "id", "name", "Any boldness level");
    populateSelect(cultureSelect, culturesRes.cultures, "id", "display_name", "Select background");
  }

  culturalToggle.addEventListener("change", () => {
    cultureSelectWrapper.classList.toggle("hidden", !culturalToggle.checked);
  });

  function getSelectedArchetypes() {
    return Array.from(archetypeContainer.querySelectorAll("input:checked")).map((i) => i.value);
  }

  function renderList(ulElement, items) {
    ulElement.innerHTML = "";
    if (items.length === 0) {
      const li = document.createElement("li");
      li.textContent = "Nothing matched your selections.";
      ulElement.appendChild(li);
      return;
    }
    items.forEach((text) => {
      const li = document.createElement("li");
      li.textContent = text;
      ulElement.appendChild(li);
    });
  }

  async function generate() {
    const params = new URLSearchParams();
    getSelectedArchetypes().forEach((a) => params.append("archetypes", a));
    if (citySelect.value) params.append("city", citySelect.value);
    if (venueSelect.value) params.append("venue", venueSelect.value);
    if (interestSelect.value) params.append("interest_level", interestSelect.value);
    if (boldnessSelect.value) params.append("boldness_level", boldnessSelect.value);
    if (culturalToggle.checked && cultureSelect.value) {
      params.append("culture", cultureSelect.value);
      params.append("include_cultural_context", "true");
    }

    generateBtn.disabled = true;
    generateBtn.textContent = "Generating...";

    try {
      const res = await fetch(`/api/generate?${params.toString()}`);
      if (!res.ok) throw new Error("Request failed");
      const data = await res.json();

      document.getElementById("result-opening").textContent =
        data.opening_line || "No match for these selections yet.";
      document.getElementById("result-followup").textContent =
        data.follow_up || "No match for these selections yet.";
      renderList(document.getElementById("result-topics"), data.topics);
      renderList(document.getElementById("result-avoid"), data.avoid);
      document.getElementById("result-date").textContent =
        data.date_idea || "No match for these selections yet.";

      const cultureSection = document.getElementById("result-culture-section");
      const cultureBox = document.getElementById("result-culture");
      if (data.cultural_context) {
        cultureSection.classList.remove("hidden");
        const ctx = data.cultural_context;
        cultureBox.innerHTML = `
          <p class="culture-heading">${ctx.display_name}</p>
          <p class="culture-sub">Conversation topics: ${ctx.conversation_topics.join(", ")}</p>
          <p class="culture-sub">Keep in mind: ${ctx.avoid_assumptions.join(" ")}</p>
        `;
      } else {
        cultureSection.classList.add("hidden");
      }

      resultsPanel.classList.remove("hidden");
    } catch (err) {
      alert("Couldn't reach the generator. Try again.");
    } finally {
      generateBtn.disabled = false;
      generateBtn.textContent = "Generate";
    }
  }

  generateBtn.addEventListener("click", generate);

  await loadOptions();
});
