/* OpenEvo CCS Lab — shared light/dark/system theme toggle.
   Pairs with the [data-theme] mechanism in tokens.css. Any page that includes
   this script and a `<button id="theme-toggle">` gets a working three-state
   toggle (system -> light -> dark -> system) that persists via localStorage.

   Contract (documented in design-system/README.md): the toggle sets/removes
   data-theme on <html> and stores the chosen mode under the localStorage key
   "oe-theme" (values: "system" | "light" | "dark"). Pages sharing an origin
   (e.g. every openevo-ccs.github.io app) share this key, so a viewer's theme
   choice on one OpenEvo app carries over to another — by design, not by
   accident. Keep the key name and value set unchanged if you fork this. */
(function () {
  var root = document.documentElement;
  var modes = ['system', 'light', 'dark'];
  var btn = document.getElementById('theme-toggle');
  if (!btn) return;
  function apply(mode) {
    if (mode === 'system') root.removeAttribute('data-theme');
    else root.setAttribute('data-theme', mode);
    btn.textContent = 'Theme: ' + mode.charAt(0).toUpperCase() + mode.slice(1);
  }
  var saved = null;
  try { saved = localStorage.getItem('oe-theme'); } catch (e) {}
  var mode = modes.indexOf(saved) > -1 ? saved : 'system';
  apply(mode);
  btn.addEventListener('click', function () {
    mode = modes[(modes.indexOf(mode) + 1) % modes.length];
    apply(mode);
    try { localStorage.setItem('oe-theme', mode); } catch (e) {}
  });
})();
