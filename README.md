
# Romanian Masters of Informatics — Static Site

# https://cnitv-rmi.netlify.app/

This repository contains a static HTML/CSS/JS version of the Romanian Masters of Informatics website. The site was converted from a Hugo-based site into a standalone static site with a small Python generator used to create the participants page from CSV source data.

This README explains how to run the site locally, regenerate the participants page, and deploy the site (example: Netlify).

## Project structure (important files)

- `index.html` — site shell and navigation shell
- `pages/` — static content pages (HTML). These are the files that the client-side loader fetches and injects into the shell.
- `assets/css/style.css` — main styles (responsive, theme variables, sponsor sizing)
- `assets/js/main.js` — client-side navigation loader, mobile nav and theme toggle
- `assets/organisers/vianu.png` — favicon & social image used in meta tags
- `assets/flags/` — team flag SVGs used on the participants page
- `csv/teams.csv` — original data source for participants
- `scripts/generate_participants.py` — small generator that converts `csv/teams.csv` into `pages/contest/participants.html`

## Local development

Requirements
- Python 3.8+ (for the generator and optionally for the simple static server)

Run the site locally (quick):

```powershell
# From the repository root
# Start a simple static server on port 8000
python -m http.server 8000
# Then open http://localhost:8000 in a browser
```

If you prefer a single-command run that regenerates the participants page and serves the site, run:

```powershell
python .\scripts\generate_participants.py; python -m http.server 8000
```

## Regenerating participants

When `csv/teams.csv` changes, re-run the generator to update `pages/contest/participants.html`:

```powershell
python .\scripts\generate_participants.py
```

The script will read `csv/teams.csv` and `assets/flags/` and write an HTML file at `pages/contest/participants.html`. Generated pages include minimal markup (team blocks, flags, leaders/students lists) and already include the client loader script so they work when opened directly in a browser.

## SEO and social previews

Basic SEO and social meta tags were added to `index.html` and point at the deployed URL (`https://cnitv-rmi.netlify.app/`) and use `assets/organisers/vianu.png` as the image for social cards. For better SEO, consider adding per-page `title` and `description` meta tags to the pages in `pages/`.

## Deployment

This is a static site and can be hosted on any static hosting provider. Example: Netlify, GitHub Pages, Vercel.

Netlify quick deploy notes:
- Create a new Netlify site from your repository.
- Build & deploy settings: no build command required (static files only). Set the publish directory to the repository root or where your static files live (root in this repo).
- Set a custom domain if you have one; Netlify will provide a default URL.

The public deployed URL used for social tags is: https://cnitv-rmi.netlify.app/

## Contributing

- If you want to add or edit pages, update the corresponding file under `pages/`.
- If you need to change participants data, update `csv/teams.csv` and run the generator.
- For sweeping Hugo shortcodes or other template artifacts, search for `{{` patterns and replace with static HTML; take care with markup that contained logic.
