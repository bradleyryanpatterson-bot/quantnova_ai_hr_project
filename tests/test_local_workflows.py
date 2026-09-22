from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def ask(question, employee_id='QNA-1001'):
    response = client.post('/chat', json={'question': question, 'employee_id': employee_id})
    assert response.status_code == 200
    return response.json()

def test_home_and_health():
    response = client.get('/')
    assert 'text/html' in response.headers['content-type']
    assert 'Your question' in response.text
    health = client.get('/health').json()
    assert health['policy_sections'] > 30
    assert health['model'] == 'not_used'

def test_vacation_calculation_and_citations():
    result = ask('Can I take five vacation days next month?')
    assert '56 hours remaining' in result['answer']
    assert '2026-09-20' in result['answer']
    assert 'not approved' in result['answer']
    assert any(c['policy_id'] == 'QNA-HR-001' for c in result['citations'])
    assert any(t['tool'] == 'check_pto_balance' for t in result['trace'])

def test_insufficient_balance():
    assert 'insufficient' in ask('Take 20 vacation days')['answer']

def test_specific_vacation_policy_question():
    result = ask('What is the vacation accrual schedule?', None)
    assert any(c['section'] == 'Accrual Schedule' for c in result['citations'])

def test_negative_duration_not_calculated():
    assert 'hours remaining' not in ask('Take -5 vacation days')['answer']

def test_temporary_benefits():
    result = ask('What benefits am I enrolled in?', 'QNA-1002')
    assert 'Temporary' in result['answer']
    assert 'No enrollment recorded' in result['answer']
    assert 'Retirement enrollment: No' in result['answer']

def test_missing_balance_does_not_invent_one():
    result = ask('What is my PTO balance?', 'QNA-1008')
    assert 'No vacation balance record' in result['answer']
    assert '96' not in result['answer']

def test_identity_mismatch_and_unknown_employee():
    assert ask('Show QNA-1002 benefits')['status'] == 'needs_clarification'
    assert ask('My benefits', 'QNA-9999')['status'] == 'not_found'

def test_sick_balance_does_not_use_vacation():
    result = ask('What is my sick leave balance?')
    assert 'cannot provide that balance' in result['answer']
    assert all(t['tool'] != 'check_pto_balance' for t in result['trace'])

def test_retrieval_and_source_link():
    result = ask('Are credentials allowed to be shared?', None)
    assert any(c['section'] == 'Accounts and Access' for c in result['citations'])
    for source in result['citations']:
        response = client.get('/policies/' + source['filename'])
        assert response.status_code == 200
        assert source['policy_id'] in response.text

def test_empty_question_and_no_evidence():
    assert client.post('/chat', json={'question': '   '}).status_code == 422
    assert 'could not find supporting' in ask('zzzzzzzz', None)['answer']

def test_no_implicit_mutation():
    assert 'does not submit' in ask('Submit five vacation days')['answer']

def test_health_reports_broken_data(monkeypatch):
    def broken(*args):
        raise ValueError('Invalid data')
    monkeypatch.setattr('app.main.records', broken)
    assert client.get('/health').status_code == 503
