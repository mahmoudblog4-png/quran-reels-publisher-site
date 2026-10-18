# Quran Reels Publisher — public preparation workspace

Existing site: https://mahmoudblog4-png.github.io/quran-reels-publisher-site/

## What works
No-login local MP4/WebM preview, browser metadata inspection, editable caption and attribution, explicit human-review declarations and local JSON manifest export. A silent original technical test card is bundled. No Quran text, timings or recitation are generated or changed here. Selected user files remain local. No third-party scripts, analytics or application API calls are used.

## What does not work
There is no TikTok OAuth backend, account connection, inbox upload, direct posting or platform readback. The local project's TikTok workflow is a pending-state stub, not a live publisher. Authenticated portal inspection found three unsupported scopes (user.info.profile, user.info.stats, video.list), no configured products and no existing sandbox. A zero-scope correction is being prepared; do not claim saved removal until readback succeeds.

Do not resubmit yet. Do not claim that these website changes meet every reviewer requirement. See `SUBMISSION_PACKAGE.md` and `review.html`. The clearly labeled `demo.html` rehearsal is simulated and is not the real sandbox video TikTok requires.

## Files
- `index.html`, `workspace.js`, `workspace.css`: actual preparation application.
- `review.html`: reviewer access, implementation/scope inventory, outstanding gates, recording checklist.
- `demo.html`, `demo.js`: simulated integration rehearsal, with no credentials, API operations or fabricated success.
- `assets/integration-rehearsal.mp4`: 64-second labeled still-frame walkthrough, not a real API or sandbox recording.
- `privacy.html`, `terms.html`: legal pages with current-deployment limitations.
- `assets/app-icon.png`: existing app branding, unchanged.
- `assets/technical-sample.mp4`: original silent technical sample, not an integration recording.
- Existing TikTok site verification text file: unchanged byte for byte.

## Focused verification
```
node --check workspace.js
node --check demo.js
python tools/verify_site.py --local
python tools/verify_site.py --live
```
The verifier checks page links/canonicals, current reviewed legal text, the original icon requirements, unchanged verification token, sample fingerprint and live deployment byte parity. Legal baselines were intentionally updated to correct unsupported integration and retention claims. Website checks are not TikTok integration evidence.

## Deployment and rollback
The existing GitHub Pages deployment serves the root of the `main` branch. Publish only reviewed site files; do not publish project databases, credentials or production media. Revert the focused website commit to roll back. Preserve the verification file and icon. No changes to the YouTube application, local production runtime, schedules or publishing workflows are needed.
