#!/usr/bin/env bash
# Create the workflow's label set on the current repo. Idempotent (--force).
# The bus is these labels — run this once per repo before booting the orchestrator.
set -euo pipefail

create() { gh label create "$1" --color "$2" --description "$3" --force; }

echo "── flow-state labels ──"
create "ready-for-impl"    "0e8a16" "Triaged, spec attached, waiting to be built"
create "in-progress"       "fbca04" "Implement agent is working (max one at a time)"
create "needs-ci"          "c5def5" "PR opened, CI running"
create "needs-review"      "1d76db" "CI finished, awaiting review agent"
create "changes-requested" "d93f0b" "Review said no — back to implement"
create "approved"          "0e8a16" "CI green AND review OK — ready to merge"
create "deploying"         "fbca04" "Merge landed, Ship/CD in flight — outcome not yet known"
create "shipped"           "5319e7" "Merged and deployed"
create "deploy-failed"     "b60205" "Ship failed — rollback then file issue"
create "blocked-human"     "e11d21" "Escalation sink — needs a human decision"

echo "── triage labels ──"
create "triage:auto"       "0e8a16" "Clear + low blast radius + testable — fully autonomous"
create "triage:critical"   "b60205" "High blast radius — human approves the merge"
create "triage:big"        "d93f0b" "Big/unclear — human approves approach before build"

echo "── attempt counter ──"
create "attempt-1"         "ededed" "Implement/review round 1"
create "attempt-2"         "d4c5f9" "Implement/review round 2"
create "attempt-3"         "b60205" "Round 3 — next reject flips to blocked-human"

echo "✅ labels ready"
