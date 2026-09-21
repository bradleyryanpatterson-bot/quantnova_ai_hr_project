from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
required = ["QuantNova AI", "QNA-"]
forbidden_extensions = {'.doc', '.docx', '.pdf'}
problems=[]
for p in ROOT.rglob('*'):
    if p.is_file() and p.suffix.lower() in forbidden_extensions:
        problems.append(f"Unexpected source document in public package: {p.relative_to(ROOT)}")
policy_text='\n'.join(p.read_text(encoding='utf-8',errors='ignore') for p in (ROOT/'policies').glob('*.md'))
if 'QuantNova AI' not in policy_text:
    problems.append('QuantNova AI branding missing from policy corpus')
if problems:
    print('PUBLISH CHECK FAILED')
    print('\n'.join(problems)); sys.exit(1)
print('PUBLISH CHECK PASSED')
