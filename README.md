# Gluten-Free Dubai

A personal tool for finding gluten-free food in Dubai when you have celiac disease.

**Rules:** no gluten, no quinoa, no oats. "Made without gluten" is fine, and so is a shared kitchen.

- `index.html` is the web page, published privately as a Claude artifact. It has three tabs:
  - **Places:** a filterable list. You can set a status on each place, keep notes, and mark places "I checked this myself".
  - **Check a menu:** paste a menu or upload screenshots, and Claude sorts each dish into fine, ask or avoid.
  - **My rules:** the editable list of things to avoid.
- `data/places/*.json` holds a snapshot of every place in the page's database, with sources and the questions to ask each restaurant.
- `tools/import_research.py` turns a research agent's JSON output into place files.

Evidence levels, strongest first: you confirmed it, the restaurant marks it GF, celiacs report it, ask first.
Most research evidence comes from search snippets of Find Me Gluten Free, Atly and press articles.
Always confirm with the restaurant.
