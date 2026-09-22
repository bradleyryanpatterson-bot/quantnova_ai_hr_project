"""QuantNova AI agent orchestration scaffold.

User-visible traces contain operational events only and never hidden chain-of-thought.
"""
from dataclasses import dataclass, field

@dataclass
class AgentState:
    employee_id: str | None
    intent: str = "unknown"
    sources: list[dict] = field(default_factory=list)
    trace: list[dict] = field(default_factory=list)
    requires_confirmation: bool = False

READ_TOOLS = {"search_policy_documents", "get_policy_section", "lookup_employee_profile", "check_pto_balance", "lookup_benefits_status", "web_search"}
WRITE_TOOLS = {"create_mock_hr_ticket"}

def answer_question(question: str, employee_id: str | None = None) -> dict:
    """Grounded local workflows; no language model or external service is used."""
    import re
    from hr_mcp import tools
    trace, citations, statements = [], [], []

    def call(name, **args):
        result = getattr(tools, name)(**args)
        trace.append({'tool': name, 'status': result['status']})
        return result

    def cite(policy_id, section):
        result = call('get_policy_section', policy_id=policy_id, section=section)
        if result['record']:
            row = result['record']
            if row not in citations:
                citations.append(row)
            return row['snippet']
        return 'This policy section is unavailable. Contact People Operations.'

    q = question.lower()
    mentioned = set(re.findall(r'QNA-\d+', question.upper()))
    selected = employee_id.upper() if employee_id else None
    if len(mentioned) > 1 or (selected and mentioned and mentioned != {selected}):
        return dict(status='needs_clarification', answer='The employee ID in your question does not match the selected demo identity. Select the matching identity and ask about one employee at a time.', citations=[], trace=[])
    identity = selected or next(iter(mentioned), None)
    pto = bool(re.search(r'\b(pto|vacation|holiday|balance)\b', q))
    benefits = bool(re.search(r'\b(benefits?|enroll\w*|insurance|dental|vision|retirement|medical plan)\b', q))
    sick = bool(re.search(r'\b(sick|personal leave)\b', q))
    profile_request = bool(re.search(r'\b(profile|department|job title|classification|who am i)\b', q))
    personal = bool(identity or re.search(r'\b(my|i|me)\b', q))
    if re.search(r'\b(submit|approve|book|create|change|cancel)\b', q):
        statements.append('This local demo provides guidance only. It does not submit requests, approve leave, or change records.')

    profile = None
    if personal and (pto or benefits or profile_request or sick):
        if not identity:
            return dict(status='needs_clarification', answer='Select a demo employee or include an ID such as QNA-1001 so I can look up the correct record.', citations=[], trace=[])
        result = call('lookup_employee_profile', employee_id=identity)
        profile = result['record']
        if not profile:
            return dict(status='not_found', answer=f'No synthetic employee record was found for {identity}. Choose an employee from the demo selector.', citations=[], trace=trace)
        statements.append(f"{profile['first_name']} {profile['last_name']} ({identity}) is a {profile['employment_type']} employee in {profile['department']}. [mock_data/employees.json]")

    if pto and not sick:
        statements.append(cite('QNA-HR-001', 'Eligibility'))
        if profile:
            result = call('check_pto_balance', employee_id=identity)
            record = result['record']
            if record:
                balance = record['available_hours']
                statements.append(f"Recorded vacation balance: {balance:g} hours as of {record['as_of_date']}. [mock_data/pto.json] This is a dated demo snapshot, not a live balance.")
                number_words = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10}
                pattern = r'\b(\d+(?:\.\d+)?|' + '|'.join(number_words) + r')\s+(?:(?:vacation|work|working)\s+)?(days?|hours?|weeks?)\b'
                amounts = list(re.finditer(pattern, q))
                if len(amounts) == 1 and not re.search(r'-\s*\d', q):
                    amount, unit = amounts[0].groups()
                    count = number_words[amount] if amount in number_words else float(amount)
                    hours = count * (40 if unit.startswith('week') else 8 if unit.startswith('day') else 1)
                    remaining = balance - hours
                    statements.append(f'Estimate: {balance:g} starting hours − {hours:g} requested hours = {remaining:g} hours remaining. Uses an eight-hour day / five-day workweek; excludes future accrual and other pending leave.')
                    if remaining < 0:
                        statements.append('The recorded balance is insufficient for this request.')
                    cite('QNA-HR-001', 'Balance and Calculation')
                else:
                    statements.append('For a balance estimate, specify one duration, for example “five vacation days” or “16 hours”.')
            else:
                statements.append('No vacation balance record is available for this employee. Contact People Operations; a balance cannot be inferred from tenure.')
        statements.append(cite('QNA-HR-001', 'Scheduling and Approval'))

    if benefits:
        statements.append(cite('QNA-HR-004', 'General Eligibility'))
        if profile:
            result = call('lookup_benefits_status', employee_id=identity)
            record = result['record']
            if record:
                statements.append(f"Benefits record as of {record['as_of_date']}: {record['status']}. [mock_data/benefits.json] This is a dated demo snapshot.")
                for key, label in [('medical_plan', 'Medical'), ('dental_plan', 'Dental'), ('vision_plan', 'Vision')]:
                    statements.append(f"{label}: {record[key] or 'No enrollment recorded'}.")
                statements.append('Retirement enrollment: ' + ('Yes.' if record['retirement_enrollment'] else 'No.'))
            else:
                statements.append('No benefits record is available. Eligibility alone does not establish enrollment; contact People Operations.')
        cite('QNA-HR-005', 'Employment Classifications')

    if sick:
        statements.append('The demo does not contain sick or personal leave balance records; I cannot provide that balance.')
        statements.append(cite('QNA-HR-002', 'Eligibility and Records'))
        statements.append(cite('QNA-HR-002', 'Notice'))

    if (pto or benefits or sick) and re.search(r'\b(accru\w*|maximum|separation|notice|documentation|privacy|changes|eligibility)\b', q):
        results = call('search_policy_documents', query=question, top_k=3)['results']
        for row in results:
            if row not in citations:
                citations.append(row)
                statements.append(f"{row['section']} [{row['policy_id']}]:\n{row['snippet']}")

    if not (pto or benefits or sick):
        results = call('search_policy_documents', query=question, top_k=3)['results']
        if results:
            statements.append('Relevant passages from the QuantNova AI policy documents:')
            for row in results:
                citations.append(row)
                statements.append(f"{row['section']} [{row['policy_id']}]:\n{row['snippet']}")
        elif not profile:
            statements.append('I could not find supporting policy evidence. Try asking about vacation, benefits, sick leave, confidentiality, security, or workplace concerns. Refer unanswered questions to People Operations.')

    return dict(status='ok', answer='\n\n'.join(statements), citations=citations,
                snippets=[r['snippet'] for r in citations], trace=trace, mode='local_grounded')

def safe_trace(tool: str, args: dict, status: str, source: str | None = None) -> dict:
    return {"tool": tool, "args": args, "status": status, "source": source}

def requires_confirmation(tool: str) -> bool:
    return tool in WRITE_TOOLS
