#!/usr/bin/env bash
# OPTIONAL self-test. Files one demo issue per triage branch so you can watch all
# three gates fire end-to-end in a fresh repo. Run after setup-labels.sh.
#
# For a REAL project you don't run this — you file real issues and triage them by
# hand (see SETUP.md). These three are deliberately generic placeholders: replace
# each body with a real spec before letting the orchestrator build it, or the
# `triage:big` restatement step will (correctly) stop and ask.
set -euo pipefail

seed() { # title  triage-label  body
  gh issue create --title "$1" \
    --label "ready-for-impl" --label "$2" --label "attempt-1" \
    --body "$3"
}

seed "[demo] auto-triage smoke test" "triage:auto" \
  "Clear, low-blast-radius, testable change. Replace this body with a real one-sentence spec whose intended diff you could describe in one line. Should ride to shipped with no human gate."

seed "[demo] critical-triage smoke test" "triage:critical" \
  "A high-blast-radius change (touches auth / schema / money / the pipeline / hard to undo). Replace with a real spec. The orchestrator should build + open a PR but STOP for human approval before merge."

seed "[demo] big-triage smoke test" "triage:big" \
  "Deliberately thin spec — no clear intended diff. Replace with a real (still-vague) request. The orchestrator should STOP and ask you to approve an approach BEFORE building."

echo "✅ demo backlog seeded"
gh issue list --state open
