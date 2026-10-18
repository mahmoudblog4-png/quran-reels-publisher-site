"use strict";
(() => {
 const steps = [
 ["1. Authorization request", "Illustration only: the future application redirects to TikTok to request only the upload permission. No redirect or consent request is performed here.", "NOT AUTHORIZED"],
 ["2. Consent and secure callback", "Illustration only: the sandbox user would approve permissions on TikTok. A real backend would verify OAuth state, exchange the code and retain tokens securely. None of this happens here.", "NO ACCOUNT CONNECTED"],
 ["3. Video preparation", "The separate workspace really previews local files and exports a manifest. This screen only describes that step; it does not inspect or upload your video.", "NO VIDEO TRANSFERRED"],
 ["4. Explicit upload confirmation", "Illustration only: after reviewing the exact file, the user would consent to a real inbox transfer. No request is made here and no approval is collected.", "UPLOAD NOT STARTED"],
 ["5. Transfer and status readback", "Illustration only: a real implementation would initialize inbox delivery, send bytes and poll the official status endpoint. No transaction identifier or successful API result exists here.", "NO API RESULT"],
 ["6. Finish in TikTok and verify", "Illustration only: the creator would open the actual inbox notification to edit and optionally post. Inbox delivery is distinct from publication. No real inbox item or post is claimed.", "NOT UPLOADED / NOT PUBLISHED"]
 ];
 let index = 0;
 function render() { const row=steps[index]; document.getElementById('step-title').textContent=row[0]; document.getElementById('step-body').textContent=row[1]; document.getElementById('step-state').textContent='SIMULATED — '+row[2]; document.getElementById('previous').disabled=index===0; document.getElementById('next').disabled=index===steps.length-1; }
 document.getElementById('previous').addEventListener('click',()=>{if(index>0)index--;render();});
 document.getElementById('next').addEventListener('click',()=>{if(index<steps.length-1)index++;render();});
})();
