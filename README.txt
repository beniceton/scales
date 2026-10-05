DEMIDOV SCALES — install as an app
==================================

This folder is a complete web app. The narration is embedded, so it works offline once opened.

1. Put the folder online (any static host; all free):
   - GitHub: create a repo, upload these files, Settings > Pages > deploy from main.
     Your link becomes https://<you>.github.io/<repo>/
   - Netlify: app.netlify.com > "Add new site" > "Deploy manually" > drag this folder in.
   - Azure Static Web Apps / any web server: upload the folder as-is.

2. Open the link on your phone and add it to the Home Screen:
   - iPhone (Safari): Share button > "Add to Home Screen" > Add.
   - Android (Chrome): three dots > "Add to Home screen" / "Install app".

It opens full-screen with its own icon, like an app.

Files: index.html (the app), manifest.webmanifest (app name, colours, icons),
icon-192.png, icon-512.png, apple-touch-icon.png.
