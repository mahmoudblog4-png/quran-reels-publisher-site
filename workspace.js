'use strict';
const SAMPLE_BYTES = 8078;
const SAMPLE_SHA256 = '6010a937a2a7a0bdf6901e08f7633ff0062b73035b90d7fe1b9e75424bdc0507';
(() => {
  const byId = id => document.getElementById(id);
  const input = byId('video-file'), preview = byId('preview'), form = byId('preparation');
  let current = null, objectUrl = null, generation = 0;
  const update = () => {
    const ready = !!current && byId('caption').value.trim().length > 0 && byId('rights').checked && byId('integrity').checked;
    byId('export').disabled = !ready;
    byId('preparation-status').textContent = ready ? 'Ready to export a LOCAL preparation manifest. No upload has occurred.' : 'Choose a playable video, add a caption and complete both review declarations.';
  };
  function clear() {
    generation++; current = null;
    preview.pause(); preview.onloadedmetadata = null; preview.onerror = null;
    preview.removeAttribute('src'); preview.load(); preview.hidden = true;
    if (objectUrl) URL.revokeObjectURL(objectUrl);
    objectUrl = null;
    byId('media-details').replaceChildren(); byId('media-details').hidden = true;
    byId('rights').checked = false; byId('integrity').checked = false; update();
  }
  function load(file, url) {
    clear();
    if (!file) { byId('media-status').textContent = 'No video selected.'; return; }
    if (!['video/mp4', 'video/webm'].includes(file.type) || !file.size || file.size > 100 * 1024 * 1024) {
      byId('media-status').textContent = 'Choose a non-empty MP4 or WebM of up to 100 MiB.'; return;
    }
    const ticket = generation;
    byId('media-status').textContent = 'Reading metadata locally…';
    objectUrl = url ? null : URL.createObjectURL(file); preview.hidden = false;
    preview.onloadedmetadata = () => {
      if (ticket !== generation) return;
      if (!Number.isFinite(preview.duration) || preview.duration <= 0 || !preview.videoWidth || !preview.videoHeight) {
        byId('media-status').textContent = 'No readable finite duration or dimensions. Export is blocked.'; return;
      }
      current = {file, duration: preview.duration, width: preview.videoWidth, height: preview.videoHeight};
      const rows = {File: file.name, Size: `${(file.size / 1048576).toFixed(2)} MiB`, Dimensions: `${current.width} × ${current.height}`, Duration: `${current.duration.toFixed(2)} seconds`, Layout: Math.abs(current.width / current.height - 9 / 16) < .02 ? 'Vertical 9:16' : 'Not 9:16 — review framing'};
      for (const [key, value] of Object.entries(rows)) {
        const dt = document.createElement('dt'), dd = document.createElement('dd');
        dt.textContent = key; dd.textContent = value; byId('media-details').append(dt, dd);
      }
      byId('media-details').hidden = false;
      byId('media-status').textContent = 'Metadata read. Play the video to check the content. Platform eligibility is not verified.'; update();
    };
    preview.onerror = () => {
      if (ticket !== generation) return;
      current = null; byId('media-details').replaceChildren(); byId('media-details').hidden = true;
      byId('media-status').textContent = 'This browser cannot decode the file. Export is blocked.'; update();
    };
    preview.src = url || objectUrl;
  }
  input.addEventListener('change', () => load(input.files[0]));
  form.addEventListener('input', update);
  byId('clear-workspace').addEventListener('click', () => { form.reset(); input.value = ''; clear(); byId('media-status').textContent = 'Workspace cleared. No media was sent to any service.'; });
  byId('sample').addEventListener('click', () => {
    input.value = '';
    // Bundled neutral sample only; no fetch, upload or account connection.
    load({name: 'technical-sample.mp4', type: 'video/mp4', size: SAMPLE_BYTES}, 'assets/technical-sample.mp4');
    byId('caption').value = 'Technical sample — no Quran text or recitation.';
    byId('attribution').value = 'Original geometric test card generated for local technical testing.';
  });
  form.addEventListener('submit', async event => {
    event.preventDefault(); update(); if (byId('export').disabled) return;
    const selected = current, ticket = generation;
    const review = Object.fromEntries(['caption','reference','attribution','rights','integrity'].map(id => [id, byId(id).type === 'checkbox' ? byId(id).checked : byId(id).value.trim()]));
    byId('export').disabled = true; byId('preparation-status').textContent = 'Preparing the local download…';
    try {
      // Bundled sample fingerprint is pinned at build time. User files are hashed locally.
      let sha256 = SAMPLE_SHA256;
      if (selected.file instanceof File) {
        const hash = await crypto.subtle.digest('SHA-256', await selected.file.arrayBuffer());
        sha256 = Array.from(new Uint8Array(hash), b => b.toString(16).padStart(2,'0')).join('');
      }
      if (ticket !== generation || current !== selected) return;
      const manifest = {schema: 'quran-reels-local-preparation-v1', created_at: new Date().toISOString(), state: 'LOCAL_PREPARATION_ONLY', tiktok: {connected:false, requested_scopes:[], api_called:false, uploaded:false, published:false}, media:{name:selected.file.name, bytes:selected.file.size, type:selected.file.type, width:selected.width, height:selected.height, duration_seconds:selected.duration, sha256}, review, limitations:['User declarations are not rights or authenticity verification.','Browser metadata does not prove TikTok acceptance.','No OAuth, upload, status fetch or publication occurred.']};
      const url = URL.createObjectURL(new Blob([JSON.stringify(manifest,null,2)], {type:'application/json'}));
      const anchor = document.createElement('a'); anchor.href = url; anchor.download = 'quran-reels-preparation.json'; anchor.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
      byId('preparation-status').textContent = 'Local manifest download requested. No TikTok upload or publication occurred.';
    } catch { byId('preparation-status').textContent = 'Could not create the manifest. No media was uploaded. Try a smaller supported file.'; }
    finally { byId('export').disabled = !(current && byId('caption').value.trim() && byId('rights').checked && byId('integrity').checked); }
  });
})();
