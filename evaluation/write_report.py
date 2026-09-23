"""Render the measured run and explicit single-evaluator review into Markdown."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
DATA=HERE/'results'/'benchmark.json'

# One-based citation positions manually reviewed against each question and source.
# Relevant means directly answers a question or supplies needed workflow context.
RELEVANT={
 'E01':[1,2], 'E02':[], 'E03':[3], 'E04':[], 'E05':[1],
 'E06':[2,3], 'E07':[1], 'E08':[1,3], 'E09':[1,3,4],
 'E10':[1,3,4,5], 'E11':[3], 'E12':[], 'E13':[1,2,3],
 'E14':[1,2,3], 'E15':[1,2], 'E16':[], 'E17':[],
 'E18':[1,2], 'E19':[], 'E20':[1,2,3], 'E21':[],
 'E22':[1,2,3], 'E23':[], 'E24':[], 'E25':[3], 'E26':[], 'E27':[], 'E28':[]}
NOTES={
 'E01':'Correct general eligibility and written exception; no personal enrollment invented.',
 'E02':'FAIL: asks for an identity instead of answering a general notice question.',
 'E03':'Correct 104 hours/year and 200-hour maximum; includes unnecessary extra policy text.',
 'E04':'FAIL: gives eligibility and scheduling passages; never states the eight-hour workday.',
 'E05':'Correct temporary-employee rule and written-agreement exception.',
 'E06':'Correctly includes no automated findings and human-review guidance, with an unrelated security citation.',
 'E07':'Correct outside-information rule; two extra citations are unrelated.',
 'E08':'Correct conflict handling; also cites benefits-specific missing/conflicting evidence.',
 'E09':'Correct Temporary classification, zero vacation hours, no enrollment, and written exceptions.',
 'E10':'Both sick-leave overlap and family/medical eligibility-review passages are present.',
 'E11':'Privacy guidance is correct, but only the sick-leave document is cited; cross-document coverage is incomplete.',
 'E12':'Correct 96-hour dated snapshot with inline JSON attribution; attached policy sections do not establish the balance.',
 'E13':'Correct 96 - 40 = 56 hours; labels estimate and preserves approval requirement.',
 'E14':'Correct 96 - 160 = -64 hours and insufficient-balance warning.',
 'E15':'Correct active plans, retirement enrollment, and record date.',
 'E16':'Correctly reports missing PTO data and directs the user to People Operations.',
 'E17':'Correctly returns not_found for the nonexistent employee.',
 'E18':'FAIL: returns generic passages without requesting leave type, identity, or dates.',
 'E19':'Correctly requests identity before personal benefits lookup.',
 'E20':'FAIL: silently selects five from two or five, calculates 40 requested hours and 56 remaining. Arithmetic is correct, but the chosen input is unsupported.',
 'E21':'Blocks the identity mismatch before any tools. This does not test real authorization.',
 'E22':'Does not approve; calculates -24 hours, flags insufficient balance and additional review.',
 'E23':'Declares guidance-only operation and performs no change; shows existing benefits.',
 'E24':'FAIL: discloses no submission, but fetches unrelated enrollment and omits the People Operations next step. Ticket creation is not supported.',
 'E25':'FAIL: safe trace contains only tool/status, but the answer does not explain the prohibition on logging medical details. Related medical intake guidance is insufficient.',
 'E26':'Correct no-evidence fallback; still invokes policy search, failing the strict no-tool routing expectation.',
 'E27':'Correct no-evidence fallback; still invokes policy search, failing the strict no-tool routing expectation.',
 'E28':'Injected OSError produces controlled HTTP 503 without invented enrollment. Exception response loses tool trace.'}
NO_FACTS={'E02','E17','E19','E21','E26','E27','E28'}

def main():
    data=json.loads(DATA.read_text(encoding='utf-8'))
    rows=data['runs']['3']; metrics=data['metrics']['3']; timing=data['timing']
    review=[]
    for row in rows:
        rid=row['id']
        review.append(dict(id=rid,grounded=None if rid in NO_FACTS else rid!='E20',
            relevant_citation_positions=RELEVANT[rid],note=NOTES[rid]))
        assert all(1<=i<=len(row['response'].get('citations',[])) for i in RELEVANT[rid])
    valid=[r for r in review if r['grounded'] is not None]
    grounded=sum(r['grounded'] for r in valid)
    relevant=sum(len(r['relevant_citation_positions']) for r in review)
    citation_count=sum(r['citation_count'] for r in rows)
    review_data=dict(reviewer='Codex, single AI-assisted qualitative review; no independent human adjudication',
        benchmark_sha256=hashlib.sha256(DATA.read_bytes()).hexdigest(),baseline_only=True,
        groundedness=dict(passed=grounded,total=len(valid)),citation_relevance=dict(relevant=relevant,total=citation_count),cases=review)
    (HERE/'results'/'qualitative_review.json').write_text(json.dumps(review_data,indent=2)+'\n',encoding='utf-8')
    unchanged=all(hashlib.sha256((HERE.parent/p).read_bytes()).hexdigest()==h for p,h in data['source_hashes'].items())
    lines=['# QuantNova AI HR Assistant: measured evaluation','',
        f"Run timestamp (UTC): {data['generated_at']}. Evaluated 28 distinct cases against the existing local app. No production code was changed. Source/data hashes still match the run: **{unchanged}**.",'',
        '**Result:** baseline k=3 satisfies 22/28 answer rubrics (78.6%). PTO arithmetic and enrollment lookup work; general-question routing, ambiguous durations, and some policy retrieval need improvement. All 16 existing unit tests also pass, showing that passing the existing tests does not establish broad answer quality.','',
        '## Scope and method','',
        '- Application: FastAPI local deterministic workflows, JSON employee records dated 2026-09-20, eight policy Markdown files, 50 section chunks, versions 2.0. No LLM, embeddings, PostgreSQL, network MCP session, external search, or hosted service is involved.',
        '- Gold answers were authored from checked-in policy and employee records. Categories cover straightforward policy, multi-document evidence, tool use, workflows, ambiguity, missing records, real fault injection, safety, and out-of-scope requests. The older questions.json is preserved as a historical draft; benchmark_cases.json is the executed set.',
        '- Each case is independent. Question and selected employee identity are both specified. E28 patches the benefits handler to raise OSError; simply claiming a tool is down in a question would not test an outage.',
        '- Automated grading checks required answer facts using explicit regex rubrics, returned tool sets, expected behavior, HTTP status, exact citation/source equality, and selected safety properties. Scores are diagnostic checks, not a general semantic evaluator.',
        '- Codex reviewed all 28 baseline responses against policies, records, calculations, and question wording. Groundedness and citation relevance below are single-evaluator judgments, not independently human-validated ratings. Qualitative review is tied to the raw result SHA-256.',
        '- Gold fact checks for E18 and E25 were tightened after output inspection to remove false positives. All three configurations were rescored consistently. This is an exploratory development benchmark, not a held-out or preregistered evaluation.','',
        '## Baseline answer and agent metrics','',
        '| Metric | Measured result | Definition / limitation |','|---|---:|---|',
        '| Complete gold-answer match | 22/28 = 78.6% | All required answer checks pass; wording is matched through explicit regex, not exact full-string equality. |',
        '| Gold fact coverage | 65/75 = 86.7% | Micro-average of required fact checks. Presence alone can overestimate semantic quality; see each response. |',
        f'| Groundedness | {grounded}/{len(valid)} = {100*grounded/len(valid):.1f}% | Answer-level review: every substantive assertion or computed input is supported. Seven control/fallback-only answers excluded. E20 fails because five days was not unambiguously requested. |',
        f'| Citation accuracy: source validity | {citation_count}/{citation_count} = 100% | Every structured policy citation matches its actual section, snippet, title, filename, and version. Does not measure relevance. |',
        f'| Citation accuracy: relevance precision | {relevant}/{citation_count} = {100*relevant/citation_count:.1f}% | Cited section directly addresses the question or provides needed workflow context. Includes otherwise valid but irrelevant citations in the denominator. |',
        '| Gold section coverage | 21/28 = 75.0% | Required policy-section hits across all gold section targets; distinct from citation relevance. JSON source references are checked through record/answer review, not this denominator. |',
        '| Tool selection accuracy | 22/27 = 81.5% | All required tool groups present; no disallowed tool type. Policy retrieval may use search or direct section lookup. E28 excluded because its HTTP error omits trace. |',
        '| Workflow completion | 10/11 = 90.9% | Tool, workflow, multi-document, and failure categories: answer checks plus expected behavior/safety and HTTP status. Controlled failure handling counts as completed handling; successful writes do not exist. E24 fails. |',
        '| Clarification / escalation handling | 7/10 = 70.0% | Ambiguity, identity mismatch, missing records, out-of-scope, unsupported action, and outage cases with explicit behavior labels. E18, E20, E24 fail. |',
        '| Action-safety pass rate | 5/5 = 100% | E21–E25: no mutation tool or false completion claim; mismatch blocks reads; medical trace uses safe fields. This is a narrow read-only safety check, not authentication or write-approval assurance. |','',
        'Tool-selection failures: E02 (unnecessary identity gate), E18 (retrieval instead of clarification), E24 (unnecessary personal reads), E26/E27 (search despite strict no-tool out-of-scope rubric). A more permissive rubric allowing policy search to establish scope would score those last two differently.','',
        'Workflow completion is rubric-based task handling, not proof that every gold section was retrieved or that an action was performed. E11 answers privacy correctly from one policy but falls short of the intended multi-document coverage. A safe refusal can pass safety while failing answer quality, as E25 does.','',
        '## Latency','',
        f"Environment: {data['platform']}; Python {data['python'].split()[0]}; CPU {data['cpu']}.",'',
        'Measured with real HTTP requests to an isolated Uvicorn process bound to 127.0.0.1. Warm sample: 15 distinct representative queries, five sequential passes (75 requests). Includes connection establishment, server work, and reading/parsing the full JSON response; excludes browser rendering. No concurrent load. Percentiles use linear interpolation. TestClient times in the raw quality results are diagnostic only and are not used for these system metrics.','',
        '| Measurement | n | p50 | p95 |','|---|---:|---:|---:|',
        f"| Warm HTTP requests | 75 | {timing['warm']['p50_ms']:.3f} ms | {timing['warm']['p95_ms']:.3f} ms |",
        f"| First HTTP query after fresh process start | 3 | {timing['cold_first_request']['p50_ms']:.3f} ms | {timing['cold_first_request']['p95_ms']:.3f} ms |",
        f"| Process launch through first response | 3 | {timing['process_start_through_response']['p50_ms']:.3f} ms | {timing['process_start_through_response']['p95_ms']:.3f} ms |",'',
        'Fresh-process tests use E13 each time. Readiness is checked by TCP connection without warming the application through /health. The OS file cache is not cleared, so these are process-cold measurements, not machine-cold measurements. With n=3, cold p95 is only descriptive. Free-tier wake-up latency is **not measured** because no deployed endpoint is configured. These local numbers do not predict LLM, database, remote MCP, production network, or concurrent-user performance.','',
        '| Representative case | Warm p50 (ms) | Warm p95 (ms) |','|---|---:|---:|']
    for rid,s in timing['warm_per_case'].items(): lines.append(f"| {rid} | {s['p50_ms']:.3f} | {s['p95_ms']:.3f} |")
    lines+=['','## Retrieval ablation','',
        'Same 28 cases and scoring rules, with search top-k forced to 1, 3, or 5 only inside the evaluation process. Direct get_policy_section calls remain unchanged. k is the number of search results, not a cap on the total answer citations. Production defaults remain k=3.','',
        '| Search k | Answer pass | Gold fact coverage | Workflow completion | Gold section coverage | Valid citations |','|---:|---:|---:|---:|---:|---:|']
    for k,m in data['metrics'].items():
        lines.append(f"| {k} | {m['answer_pass']['passed']}/28 ({m['answer_pass']['percent']:.1f}%) | {m['gold_fact_recall_percent']:.1f}% | {m['workflow_completion']['passed']}/11 | {m['gold_section_recall']['found']}/28 | {m['citation_source_fidelity']['valid']}/{m['citation_source_fidelity']['total']} |")
    lines+=['',
        'k=3 recovers E06 (misconduct limits) and E10 (leave overlap) compared with k=1. k=5 additionally recovers E25 through the family/medical confidentiality section. It increases citations from 63 to 77 but does not fix E02, E04, E18, E20, or E24. Gold target coverage stays unchanged because the E25 logging answer is supported by an alternative relevant section. Manual relevance/groundedness ratings were applied only to the baseline. No controlled latency comparison across k values was performed.','',
        '## Questions, gold answers, and observed results','',
        'Employee IDs: QNA-1001 = Maya Chen; QNA-1002 = Jordan Lee; QNA-1008 = Priya Nair. None means no employee was selected. Full responses, citations, and tool traces follow in [responses.md](responses.md).','',
        '| ID / category | Question / identity | Gold answer | Observed result |','|---|---|---|---|']
    for r in rows:
        clean=lambda s:s.replace('|','/').replace('\n',' ')
        lines.append(f"| {r['id']} / {r['category']} | {clean(r['question'])} **[{r['employee_id'] or 'None'}]** | {clean(r['gold_answer'])} | **{'PASS' if r['completion_pass'] else 'FAIL'}** — {NOTES[r['id']].removeprefix('FAIL: ')} |")
    lines+=['','## Recommended fixes, in order','',
        '1. Detect alternative durations before calculating PTO. E20 currently presents one interpretation as the requested amount.',
        '2. Separate general policy questions from personal record requests. E02 should not require identity; E04 needs the standard-workday section.',
        '3. Ask targeted clarification for broad time-off requests instead of returning loosely matching passages (E18).',
        '4. Route unsupported ticket actions to an explicit no-ticket-created response and People Operations without unrelated enrollment reads (E24).',
        '5. Improve retrieval relevance and explicit privacy guidance. k=5 helps E25 but also adds text; routing/ranking changes should be evaluated on a new held-out set.',
        '6. If evolving beyond a demo, separately evaluate authenticated authorization, actual write confirmation, PostgreSQL/remote tool failures, concurrent load, and deployed cold starts. None is established by these results.','',
        '## Reproduce','',
        'From Command Prompt in the project directory:','',
        '```cmd',
        'cd /d "C:\\Users\\nicho\\OneDrive\\Documents\\quantnova_ai_hr_project"',
        '.venv\\Scripts\\python.exe -m evaluation.run_benchmark',
        '.venv\\Scripts\\python.exe -m pytest -q',
        '```','',
        'The benchmark writes benchmark_cases.json and results/benchmark.json and starts/stops its own temporary local servers. It does not need the UI server running. Qualitative review and this report describe the saved run: after app/policy changes, re-review baseline answers and update write_report.py annotations before regenerating the report with `python -m evaluation.write_report`. Do not reuse the manual ratings blindly.','']
    (HERE/'REPORT.md').write_text('\n'.join(lines),encoding='utf-8')
    full=['# Complete baseline responses','',f"Run: {data['generated_at']}; search k=3.",'']
    for r in rows:
        full += [f"## {r['id']}: {r['question']}",'',f"Category: {r['category']}; selected identity: {r['employee_id'] or 'None'}; HTTP {r['http_status']}.",'',
            '**Gold:** '+r['gold_answer'],'','**Assessment:** '+NOTES[r['id']],'','**Actual answer:**','',r['response'].get('answer',r['response'].get('detail','')),'',
            '**Actual tool trace:**','', '```json',json.dumps(r['response'].get('trace',[]),indent=2),'```','',
            '**Structured policy citations:**','']
        for i,c in enumerate(r['response'].get('citations',[]),1):
            full.append(f"- {i}. {c['policy_id']}, {c['section']}, v{c['version']}; {c['filename']}. Relevance: {'yes' if i in RELEVANT[r['id']] else 'no'}.")
        if not r['response'].get('citations'):full.append('None.')
        full+=['']
    (HERE/'responses.md').write_text('\n'.join(full),encoding='utf-8')
    print(json.dumps(dict(groundedness=review_data['groundedness'],citation_relevance=review_data['citation_relevance'],source_hashes_unchanged=unchanged)))

if __name__=='__main__':main()
