import argparse
from src.data_loader import get_legislator
from src.embeddings import embed_legislator
from src.retriever import retrieve_votes
from src.generator import generate_brief

def main():
    parser = argparse.ArgumentParser(description="Generate a legislative climate brief.")
    parser.add_argument("--legislator", required=True, help="Legislator full name")
    parser.add_argument("--state", default=None, help="State abbreviation (optional)")
    args = parser.parse_args()

    print(f"Loading data for {args.legislator}...")
    legislator = get_legislator(args.legislator, args.state)

    print("Embedding voting records into vector database...")
    embed_legislator(legislator)

    print("Retrieving relevant voting records...")
    records = retrieve_votes(args.legislator)

    print("Generating brief with Claude...")
    brief = generate_brief(legislator, records)

    print("\n" + "="*50)
    print(f"LEGISLATIVE BRIEF: {legislator['name']} ({legislator['party']} - {legislator['state']})")
    print("="*50)
    print(brief)

if __name__ == "__main__":
    main()