import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
const root = path.resolve('dist');
async function walk(dir) {
  const entries = await fs.readdir(dir, {withFileTypes: true});
  return (await Promise.all(entries.map(e => e.isDirectory() ? walk(path.join(dir, e.name)) : path.join(dir, e.name)))).flat();
}
const files = await walk(root);
const references = new Set();
for (const file of files.filter(p => /\.(html|css)$/.test(p))) {
  const text = await fs.readFile(file, 'utf8');
  for (const match of text.matchAll(/\/(?:assets|v|apple-watch-se-3|ac|api-www|wss|105)\/[^\s"'<>()[\]]+?\.(?:jpg|jpeg|png|svg|gif|ico|css|js|woff2?|ttf|mp4|webm)/g)) references.add(match[0]);
}
const missing = [];
for (const resource of references) {
  try { await fs.access(path.join(root, resource)); } catch { missing.push(resource); }
}
assert.deepEqual(missing, [], 'All HTML/CSS resources must exist locally.');
const html = await fs.readFile(path.join(root, 'index.html'), 'utf8');
assert.equal((html.match(/<h1\b/g) || []).length, 1, 'Exactly one primary heading.');
assert.ok(/data-localnav-trigger-anchor=["']?\.rh-price-action/.test(html), 'Native localnav trigger must remain present.');
assert.ok(/lang="fa"/.test(html) && /dir="rtl"/.test(html), 'Persian must be the static default.');
const english = await fs.readFile(path.join(root, 'en/index.html'), 'utf8');
assert.ok(/lang="en-US"/.test(english) && /dir="ltr"/.test(english), 'English route must retain LTR.');
for (const weight of ['Light','Regular','Medium','Bold']) await fs.access(path.join(root,'assets/pinar',`Pinar-DS4-${weight}.woff2`));
assert.doesNotMatch(html, /Starting at\s*\$229|data-toggle="acmi"/);
for (const tag of html.match(/<video\b[^>]*>/g) || []) {
  const base = tag.match(/data-inline-media-basepath="([^"]+)"/)?.[1];
  if (!base) continue;
  const disabled = (tag.match(/data-inline-media-retina-disabled-viewports="([^"]+)"/)?.[1] || '').split(',');
  for (const size of ['large','medium','small']) {
    await fs.access(path.join(root, base, size + '.mp4'));
    if (!disabled.includes(size)) await fs.access(path.join(root, base, size + '_2x.mp4'));
  }
}
for (const size of ['large_2x','medium_2x','small_2x']) await fs.access(path.join(root, 'assets', 'hero-' + size + '.mp4'));
const config = JSON.parse(await fs.readFile('.openai/hosting.json', 'utf8'));
assert.equal(config.static.directory, 'dist');
assert.ok(config.project_id);
console.log(`PASS: ${files.length} files, ${references.size} local HTML/CSS resources, responsive media, heading and hosting configuration.`);
