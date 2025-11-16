param(
  [string]$Repo,
  [datetime]$StartDate = (Get-Date),
  [switch]$DryRun,
  [switch]$AssignAgentMilestones,
  [switch]$AssignOnly
)

function Ensure-Gh {
  if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI 'gh' not found. Install: https://cli.github.com and run 'gh auth login'."
  }
}

function Get-RepoNameWithOwner {
  param([string]$Repo)
  if ($Repo) { return $Repo }
  try {
    $r = gh repo view --json nameWithOwner -q ".nameWithOwner" 2>$null
    if ($LASTEXITCODE -eq 0 -and $r) { return $r.Trim() }
  } catch {}
  throw "Repository not detected. Pass -Repo <owner/name> or run from within a GH repo."
}

function Ensure-Label {
  param([string]$Name,[string]$Color="0366d6",[string]$Description="")
  $exists = gh label list --limit 200 --json name -q ".[] | select(.name==\"$Name\") | .name" 2>$null
  if ($DryRun) { Write-Host "DRYRUN label $Name"; return }
  if (-not $exists) { gh label create "$Name" --color $Color --description "$Description" | Out-Null }
}

function Ensure-Milestone {
  param([string]$RepoNWO,[string]$Title,[string]$Description,[datetime]$DueOn)
  $num = gh api repos/$RepoNWO/milestones -f state=all -q ".[] | select(.title==\"$Title\") | .number" 2>$null
  if ($num -and ($num.Trim() -match '^[0-9]+$')) { return [int]$num.Trim() }
  if ($DryRun) { Write-Host "DRYRUN milestone $Title"; return $null }
  $iso = $DueOn.ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  $created = gh api repos/$RepoNWO/milestones -X POST -f title="$Title" -f description="$Description" -f due_on="$iso" --jq ".number" 2>&1
  if ($LASTEXITCODE -ne 0 -or -not $created -or ($created.Trim() -notmatch '^[0-9]+$')) {
    Write-Warning "Failed to create milestone '$Title' for $RepoNWO. Ensure repo exists and you have access. Output: $created"
    return $null
  }
  return [int]$created.Trim()
}

function New-Issue {
  param([string]$RepoNWO,[string]$Title,[string]$Body,[string[]]$Labels,[string]$MilestoneName)
  $labelArgs = @()
  foreach ($l in $Labels) { if ($l) { $labelArgs += @("--label",$l) } }
  $msArgs = @()
  if ($MilestoneName) { $msArgs = @("--milestone",$MilestoneName) }
  if ($DryRun) { Write-Host "DRYRUN issue: $Title"; return }
  gh issue create --repo $RepoNWO --title "$Title" --body "$Body" @labelArgs @msArgs | Out-Null
}

function Get-IssueNumberByTitle {
  param([string]$RepoNWO,[string]$Title)
  try {
    $n = gh issue list --repo $RepoNWO --state open --search "in:title $Title" --json number,title -q ".[] | select(.title==\"$Title\") | .number" 2>$null
    if ($n -and ($n.Trim() -match '^[0-9]+$')) { return [int]$n.Trim() }
  } catch {}
  return $null
}

Ensure-Gh
$repoNWO = Get-RepoNameWithOwner -Repo $Repo

# Labels
$labels = @(
  @{ n='type:task'; c='6f42c1'; d='Work task' },
  @{ n='type:epic'; c='cfd3d7'; d='Epic/umbrella issue' },
  @{ n='area:extension'; c='0e8a16'; d='VS Code extension' },
  @{ n='area:backend'; c='1d76db'; d='Python backend' },
  @{ n='area:contracts'; c='5319e7'; d='Shared contracts' },
  @{ n='area:tests'; c='5319e7'; d='Testing' }
)
1..14 | ForEach-Object { $labels += @{ n=("agent:" + $_.ToString("00")); c='d93f0b'; d='Agent assignment' } }
foreach ($l in $labels) { Ensure-Label -Name $l.n -Color $l.c -Description $l.d }

# Milestones (Weeks 1..10)
$weekTitles = @(
  'Week 1 — Foundations & Bootstrap',
  'Week 2 — Contracts & Messaging',
  'Week 3 — Indexing I (Discovery, Documentation)',
  'Week 4 — Indexing II (Structure, Chunking)',
  'Week 5 — Embeddings & Vector Search',
  'Week 6 — Retrieval Pipeline & Chat Integration',
  'Week 7 — Plans View',
  'Week 8 — Act Mode (Safe Execution)',
  'Week 9 — Hardening & Coverage',
  'Week 10 — Release Readiness'
)
$weekDescs = @(
  'Initialize repo, scaffold extension/backend, register Chat + Views, CI green.',
  'Shared models, WS envelope, health/config endpoints, stubs.',
  'Discovery + docs extraction + metadata store + progress events.',
  'AST structure, symbols, AST-first chunking + lexical fallback.',
  'Ollama bge-m3 embeddings, Chroma vector search, filters.',
  'Multi-level retrieval + fusion, Chat streaming, Transfer to Plan.',
  'Plan CRUD, persistence, tree rendering.',
  'Dry-run diffs, approvals, Git safety, apply/rollback.',
  'Edge cases, perf checks, regression, VRAM monitor/swapper.',
  'Docs, onboarding, packaging, templates; nightly E2E stable.'
)

$weekMilestones = @{}
for ($i=0; $i -lt $weekTitles.Count; $i++) {
  $due = $StartDate.AddDays(7*($i+1))
  if ($AssignOnly) {
    # In assign-only mode, do not attempt to create milestones; just use titles.
    $weekMilestones["W$($i+1)"] = $weekTitles[$i]
  } else {
    $null = Ensure-Milestone -RepoNWO $repoNWO -Title $weekTitles[$i] -Description $weekDescs[$i] -DueOn $due
    $weekMilestones["W$($i+1)"] = $weekTitles[$i]
  }
}

function WeekBody($deliverables,$gates) {
  return "Deliverables:`n- " + ($deliverables -join "`n- ") + "`n`nAcceptance Gates:`n- " + ($gates -join "`n- ")
}

# Epic issues per week
$weeks = @(
  @{ k='W1'; t='[W1] Foundations & Bootstrap'; d=@('Initialize repo structure','Scaffold extension (strict TS, ESLint, Jest, engines>=1.88)','Scaffold backend (pyproject/requirements, flake8/ruff, pytest)','Register Chat participant and Views container','CI on Windows with lint/type/test','Add CODEOWNERS and templates'); g=@('Extension loads; Views visible','Chat participant registered','CI green on Windows','Contracts compile') },
  @{ k='W2'; t='[W2] Contracts & Messaging'; d=@('Shared TS/Pydantic models','WebSocket envelope and router','Health + config REST','Stub services'); g=@('Round-trip WS ping','Health endpoint returns 200','Types compile','Unit tests >= 70% for contracts') },
  @{ k='W3'; t='[W3] Indexing I (Discovery, Docs)'; d=@('Discovery executor','Ignore rules','Doc extraction','Metadata store with file hash cache','Indexing progress events'); g=@('Index small repo','Progress visible in Indexing view','Unit tests >= 75%') },
  @{ k='W4'; t='[W4] Indexing II (Structure, Chunking)'; d=@('Tree-sitter structure','Symbol/import map','AST-first chunking','Lexical fallback path'); g=@('Deterministic chunk boundaries','Partial-ready events emitted','Precision checks on boundaries') },
  @{ k='W5'; t='[W5] Embeddings & Vector Search'; d=@('Ollama bge-m3 embeddings','Chroma upsert/query','Index maintenance','Filters'); g=@('Coherent neighbors','Retrieval metrics logged','Unit+integration >= 80% for RAG infra') },
  @{ k='W6'; t='[W6] Retrieval & Chat Integration'; d=@('Multi-level retrieval + fusion/ranking','Chat streaming integration','Transfer to Plan command'); g=@('Grounded chat answers','Plan suggestions visible','Integration tests pass') },
  @{ k='W7'; t='[W7] Plans View'; d=@('Plan model and storage','CRUD + reorder','Tree rendering','Acceptance criteria model'); g=@('Plan steps editable','Keyboard navigation','Tests >= 80% for Plan components') },
  @{ k='W8'; t='[W8] Act Mode (Safe Execution)'; d=@('Dry-run diff preview','Git safety checks','Approval workflow','Apply + rollback'); g=@('Cannot apply without approval','Blocked outside Git repo unless override','Integration tests pass') },
  @{ k='W9'; t='[W9] Hardening & Coverage'; d=@('Edge cases','Performance checks','Regression suite','VRAM monitor + swapper'); g=@('Overall coverage >= 85% (critical >= 85%)','Type coverage 100%','No cyclic dependencies','Perf smoke passes') },
  @{ k='W10'; t='[W10] Release Readiness'; d=@('Final docs','Onboarding','VSIX packaging','Issue templates'); g=@('Nightly E2E green 5 days','Windows smoke OK','Acceptance sign-off') }
)

foreach ($w in $weeks) {
  $body = WeekBody $w.d $w.g
  $msName = $weekMilestones[$w.k]
  if ($AssignOnly) {
    $num = Get-IssueNumberByTitle -RepoNWO $repoNWO -Title $w.t
    if ($DryRun) { Write-Host "DRYRUN assign milestone to existing: $($w.t) -> $msName" }
    elseif ($num) { gh issue edit $num --repo $repoNWO --milestone "$msName" | Out-Null }
  } else {
    New-Issue -RepoNWO $repoNWO -Title $w.t -Body $body -Labels @('type:epic') -MilestoneName $msName
  }
}

# Agent issues
$agentMilestones = @{
  '01'='W1';
  '02'='W1';
  '03'='W6';
  '04'='W2';
  '05'='W2';
  '06'='W3';
  '07'='W4';
  '08'='W5';
  '09'='W6';
  '10'='W7';
  '11'='W8';
  '12'='W9';
  '13'='W9';
  '14'='W10'
}
$agents = @(
  @{ id='01'; title='Agent 01 — Repo Architecture & Tooling'; labels=@('area:extension','area:backend','agent:01'); body='Set up repo structure, strict configs, CI, VS Code tasks/launch. Deliver ESLint/Prettier/tsconfig; flake8/ruff/pytest; CI workflows.' },
  @{ id='02'; title='Agent 02 — Extension Views & Commands'; labels=@('area:extension','agent:02'); body='Implement localpilot.views container, TreeDataProviders, commands, icons, keybindings; Show LocalPilot views command; tests.' },
  @{ id='03'; title='Agent 03 — Chat Participant'; labels=@('area:extension','agent:03'); body='Register localpilot participant; streaming markdown; Transfer to Plan action; integration tests.' },
  @{ id='04'; title='Agent 04 — WebSocket Client & Contract'; labels=@('area:extension','area:contracts','agent:04'); body='WS client with reconnect/backoff/heartbeat; message envelope; router; error states; unit tests.' },
  @{ id='05'; title='Agent 05 — Backend API Gateway'; labels=@('area:backend','agent:05'); body='FastAPI WS + REST; schema validation; logging; config; health + config endpoints; unit/integration tests.' },
  @{ id='06'; title='Agent 06 — Indexing: Discovery & Docs'; labels=@('area:backend','agent:06'); body='Discovery walker, ignore rules, doc extraction, metadata store, progress events; unit tests.' },
  @{ id='07'; title='Agent 07 — Indexing: Structure & Chunking'; labels=@('area:backend','agent:07'); body='Tree-sitter parse, symbol/import maps, AST-first chunking, lexical fallback; unit tests.' },
  @{ id='08'; title='Agent 08 — Embeddings & Vector Store'; labels=@('area:backend','agent:08'); body='Ollama bge-m3 integration, Chroma upsert/query, index maintenance, filters; tests.' },
  @{ id='09'; title='Agent 09 — Retrieval & Ranking'; labels=@('area:backend','agent:09'); body='Multi-level retrieval, fusion, diversity re-rank, metrics harness; integration tests.' },
  @{ id='10'; title='Agent 10 — Plan Mode'; labels=@('area:extension','agent:10'); body='Plan CRUD, persistence, tree rendering, from-Chat conversion; tests.' },
  @{ id='11'; title='Agent 11 — Act Mode (Safe Execution)'; labels=@('area:extension','area:backend','agent:11'); body='Dry-run diffs, approval workflow, Git safety, apply/rollback; integration tests.' },
  @{ id='12'; title='Agent 12 — Integration & E2E'; labels=@('area:tests','agent:12'); body='Cross-component tests, fixtures, nightly E2E scenario.' },
  @{ id='13'; title='Agent 13 — Testing & Coverage'; labels=@('area:tests','agent:13'); body='Fill coverage gaps, edge cases, performance, regression packs; enforce gates.' },
  @{ id='14'; title='Agent 14 — Docs & DX'; labels=@('agent:14'); body='Maintain docs, changelogs, contribution guide, onboarding; Windows polish.' }
)

foreach ($a in $agents) {
  $title = $a.title
  $body = $a.body
  $id = $a.id
  $msName = $null
  if ($AssignAgentMilestones) {
    $wk = $agentMilestones[$id]
    if ($wk) { $msName = $weekMilestones[$wk] }
  }
  if ($AssignOnly) {
    $num = Get-IssueNumberByTitle -RepoNWO $repoNWO -Title $title
    if ($DryRun) { Write-Host "DRYRUN assign milestone to existing: $title -> $msName" }
    elseif ($num -and $msName) { gh issue edit $num --repo $repoNWO --milestone "$msName" | Out-Null }
  } else {
    New-Issue -RepoNWO $repoNWO -Title $title -Body $body -Labels $a.labels -MilestoneName $msName
  }
}

Write-Host "Seed complete. Use -DryRun to preview."
