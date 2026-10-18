# Existing TikTok app: Quran Reels Publisher

Status: BLOCKED — NOT READY FOR RESUBMISSION
Reviewed: 2026-10-18. No TikTok approval, portal configuration update or API success is claimed.

## Root causes independently found
1. The previous public site was informational, with legal-page buttons rather than an application entry point. It described connected publishing without a working public interaction.
2. The existing project's `n8n_workflows/quran-reels-tiktok-publisher.json` only returns pending/approval-required states, has no TikTok HTTP transfer, no authorization callback and no actual platform readback. The current app sources have no TikTok OAuth routes or client implementation.
3. There is no verified sandbox transaction or complete real end-to-end integration recording. A description or a simulation cannot establish it.
4. Additional eligibility gate: app-review guidance excludes private/personal applications and apps still in development/testing. Direct Post guidance excludes utilities limited to accounts the developer/team manages. Do not conceal the current audience or invent a public service.

## Website changes
The existing domain now hosts a functional local preparation workspace: preview, dimensions/duration, caption/attribution, review declarations and a file-fingerprinted manifest download. Unsupported integration claims were corrected and the legal pages now state actual public data flows. The existing verification file and icon are preserved.

This addresses the lack of a usable public preparation surface, but TikTok can still reject a preparation-only website without a complete real TikTok integration. Acceptance of the website requirement is not established.

## Exact public URLs
Website: https://mahmoudblog4-png.github.io/quran-reels-publisher-site/
Privacy: https://mahmoudblog4-png.github.io/quran-reels-publisher-site/privacy.html
Terms: https://mahmoudblog4-png.github.io/quran-reels-publisher-site/terms.html
Reviewer instructions: https://mahmoudblog4-png.github.io/quran-reels-publisher-site/review.html
Clearly labeled simulated rehearsal: https://mahmoudblog4-png.github.io/quran-reels-publisher-site/demo.html
Technical sample (not integration evidence): https://mahmoudblog4-png.github.io/quran-reels-publisher-site/assets/technical-sample.mp4

## Products and scope inventory
- Implemented public TikTok products: NONE.
- Scopes requested by deployed website: NONE.
- Actual current portal products/scopes: UNVERIFIED (login required).
- Future minimum proposal: Login Kit authorization for a real Content Posting API inbox-upload integration using `video.upload`. Verify the exact supported sandbox configuration first. OAuth still requires a secure backend.
- Remove `video.publish` if direct posting will not be implemented and demonstrated. No direct-post feature exists today.
- Remove `video.list`, Display API and profile permissions if no required implemented feature uses them. Do not request `user.info.basic` merely to pad the demonstration; request it only if the final real account-profile feature needs and demonstrates it.
- Do not blindly delete scopes needed by an actual current feature. First compare the authenticated saved configuration, every call and the final recording; no deletion has occurred in this task.
- Zero scopes is an accurate current-site inventory, not a recommendation to submit an integration-free app.

## Submission text: safe current description
"Quran Reels Publisher provides a browser-based workspace for creators to preview their own prepared videos, inspect media dimensions and duration, edit captions and attribution, and export a local preparation manifest. The current public deployment does not yet connect to TikTok or upload media."

This accurate description explains why the app is NOT production-review-ready. Do not submit it as a claim of completed integration.

## Conditional future description — use ONLY after implementation and proof
"Quran Reels Publisher lets creators preview a prepared video and explicitly send it to their own TikTok inbox. The creator authorizes the account through TikTok Login Kit, reviews the exact media and confirms the transfer. Content Posting API with video.upload delivers the file to the TikTok inbox. The application reads the real transfer status and tells the creator to open the inbox notification to finish editing and posting in TikTok. It does not post automatically."

Do not use this paragraph while the integration remains missing. Confirm the actual audience is eligible and adjust the description to real product behavior.

## Complete demonstration storyboard
The sequence below must be RECORDED from the actual sandbox integration. The rehearsal page is not proof.
1. 00:00–00:15: show the existing app identity and Sandbox mode, selected products/scopes (mask secrets).
2. 00:15–00:35: open the exact submitted public website, visible legal links and real workspace.
3. 00:35–01:00: real TikTok authorization request, requested permissions, test user's consent and return to the application's secure callback. Hide codes/tokens.
4. 01:00–01:25: verify the actual connected identity using an implemented, authorized mechanism. Preview a rights-cleared video, inspect constraints and edit attribution/metadata.
5. 01:25–01:45: show cancellation/no-upload behavior, then explicit approval of the exact video for one bounded sandbox transfer.
6. 01:45–02:15: show actual inbox init, byte transfer and status fetch with a redacted receipt. If transfer fails, record the failure honestly; fix before submitting.
7. 02:15–02:45: show the actual inbox notification and received video in TikTok. Do not call inbox delivery publication. Completing a post needs separate explicit approval.
8. 02:45–03:00: show each requested scope's feature and final evidence status. Do not splice simulated successful API operations into this footage.

First approval requires Sandbox. Up to 5 demo files, each <=50 MB; show readable UI, actual user interactions and the same web domain as Website URL. Test credentials are unnecessary for the public local workspace. If a later real integration needs an application test account, provide access only via TikTok's private review fields; never disclose social login passwords, app secrets, OAuth tokens or production credentials.

## Remaining manual steps / authenticated portal workflow
1. Sign in to https://developers.tiktok.com/apps/ and open ONLY the existing app named Quran Reels Publisher. Do not create a new app. Record its actual saved products, scopes, registered redirect URI and latest rejection details without recording keys or secrets.
2. Resolve actual intended audience and eligibility. A private owner-only utility must not be described as public. A change to a genuine public product is a separate product/hosting implementation, not a wording correction.
3. Deploy the secure OAuth and inbox-upload service for the existing app. Preserve client identity/credentials. Use state validation, server-side code exchange, protected token storage, callback allowlisting, explicit per-file consent, bounded transfer, duplicate protection and status readback. GitHub Pages cannot host this backend. Do not expose the existing local production service or embed secrets in JavaScript.
4. In the EXISTING app's Sandbox configuration, verify the registered callback and authorized test account. Confirm only the products/scopes implemented by the final flow are selected.
5. Obtain approval for the exact account/media/mode of one sandbox transfer. No such upload has been approved or executed during this task. Record the full real demonstration and save sanitized API evidence plus the actual inbox result.
6. In the existing production app's app details, verify Website, Privacy Policy and Terms URLs against the live URLs above, and verify the existing icon/URL-property verification without replacing credentials.
7. In products/scopes, remove unsupported requested features ONLY after inspecting the saved state. Save and reopen to verify. Do not claim permission removal from a website-only code change.
8. In review information, explain every requested product and scope using actual demonstrated behavior. Attach the real sandbox video(s), accurate reviewer instructions and only genuinely needed private test-access details. Do not attach the simulated rehearsal as successful integration evidence.
9. Recheck all gates. Submit the existing app only when no required item is missing. Record the portal's actual submission confirmation and status; it is not approval.

## Official sources checked
https://developers.tiktok.com/doc/app-review-guidelines
https://developers.tiktok.com/doc/content-sharing-guidelines
https://developers.tiktok.com/doc/content-posting-api-get-started-upload-content

## Preservation boundary
No YouTube Shorts or Long-Form pipeline, production database, media, OAuth credential, publishing schedule or automation was changed. No upload or public post was triggered. No new TikTok application was created. Portal login was unavailable at initial inspection; no portal write or resubmission is claimed.
