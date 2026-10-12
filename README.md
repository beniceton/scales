# Demidov Scales

The app lives at `index.html` and is built automatically. Do not edit `index.html` by hand.

- **Change the script, perceptions or narrators:** open `studio.html` on the live site, edit, Publish. Or edit `src/script.json` directly on GitHub.
- **What happens next:** the "Build and release" Action generates narration for any new lines (ElevenLabs, only lines that don't already have a clip), rebuilds `index.html`, commits it, and GitHub Pages publishes it. Phones update themselves on next launch.
- **Design or behaviour changes:** edit `src/template.html`. Same Action, same release.
- **Clips:** `clips/<voice_id>/<line_id>.mp3`. Keeping them in the repo means a line is only ever paid for once.

Secrets: `ELEVENLABS_API_KEY` under Settings → Secrets and variables → Actions.
