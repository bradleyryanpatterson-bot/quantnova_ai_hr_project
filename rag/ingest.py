"""QuantNova AI policy ingestion scaffold for PostgreSQL + pgvector."""
from pathlib import Path

POLICY_DIR = Path(__file__).resolve().parents[1] / "policies"

def policy_files():
    return sorted(POLICY_DIR.glob("*.md"))

def main():
    files = policy_files()
    print(f"QuantNova AI policies ready for indexing: {len(files)}")
    # Integration step: parse headings, chunk, embed, upsert with deterministic policy/chunk IDs.

if __name__ == "__main__":
    main()
