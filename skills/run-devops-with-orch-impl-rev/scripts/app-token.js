#!/usr/bin/env node
// Mint a short-lived GitHub App *installation token* so an agent can act as a
// bot (a distinct identity from the human PR author). Zero dependencies —
// RS256 JWT via node:crypto, installation lookup + token via global fetch.
//
// Usage (values come from .bot-env.<role>, which is gitignored):
//   APP_ID=123456 APP_PRIVATE_KEY_PATH=~/path/key.pem REPO=owner/repo node .orchestrator/app-token.js
// Prints the installation token to stdout. Use it as:  GH_TOKEN=$(… app-token.js) gh pr review …
const crypto = require('crypto');
const fs = require('fs');

const b64url = (s) => Buffer.from(s).toString('base64url');

function makeJwt(appId, privateKey) {
  const now = Math.floor(Date.now() / 1000);
  const header = { alg: 'RS256', typ: 'JWT' };
  const payload = { iat: now - 60, exp: now + 9 * 60, iss: appId }; // clock-skew slack; <10 min
  const data = `${b64url(JSON.stringify(header))}.${b64url(JSON.stringify(payload))}`;
  const sig = crypto.sign('RSA-SHA256', Buffer.from(data), privateKey);
  return `${data}.${b64url(sig)}`;
}

const hdrs = (tok) => ({
  Authorization: `Bearer ${tok}`,
  Accept: 'application/vnd.github+json',
  'X-GitHub-Api-Version': '2022-11-28',
  'User-Agent': 'orch-impl-review',
});

async function main() {
  const appId = must('APP_ID');
  const keyPath = must('APP_PRIVATE_KEY_PATH').replace(/^~/, process.env.HOME);
  const repo = must('REPO'); // owner/repo
  const privateKey = fs.readFileSync(keyPath, 'utf8');
  const jwt = makeJwt(appId, privateKey);

  let installationId = process.env.INSTALLATION_ID;
  if (!installationId) {
    const r = await fetch(`https://api.github.com/repos/${repo}/installation`, { headers: hdrs(jwt) });
    if (!r.ok) throw new Error(`installation lookup failed: ${r.status} ${await r.text()}`);
    installationId = (await r.json()).id;
  }
  const r = await fetch(`https://api.github.com/app/installations/${installationId}/access_tokens`, {
    method: 'POST',
    headers: hdrs(jwt),
  });
  if (!r.ok) throw new Error(`token mint failed: ${r.status} ${await r.text()}`);
  process.stdout.write((await r.json()).token);
}

function must(name) {
  const v = process.env[name];
  if (!v) throw new Error(`missing env: ${name}`);
  return v;
}

main().catch((e) => { console.error('app-token error:', e.message); process.exit(1); });
