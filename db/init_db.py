"""Database initialization notes for QuantNova AI HR Assistant."""
from pathlib import Path

def main():
    schema = Path(__file__).with_name("schema.sql")
    print(f"Apply schema from: {schema}")
    print("Then load mock_data/seed.sql and run rag.ingest.")

if __name__ == "__main__":
    main()
