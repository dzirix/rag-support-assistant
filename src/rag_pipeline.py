#!/usr/bin/env python3
"""
Projet personnel — données fictives.
Prototype RAG (Retrieval-Augmented Generation) 100 % local et simulé.

Pipeline illustré :
  1. Chargement   : lecture des documents Markdown de knowledge-base/
  2. Chunking     : découpage par section (titres ##), un chunk = une section
  3. Recherche    : score de recouvrement lexical question <-> chunk
  4. Génération   : SIMULÉE — la réponse est construite à partir du passage
                    retrouvé (en production, ce passage serait fourni comme
                    contexte à un modèle de langage, avec la même consigne
                    de n'utiliser que le contexte).

Aucune clé API, aucune dépendance externe : bibliothèque standard uniquement.
Usage : python3 src/rag_pipeline.py "Combien de temps le code SMS est-il valable ?"
"""

import re
import sys
import unicodedata
from pathlib import Path

KB_DIR = Path(__file__).resolve().parent.parent / "knowledge-base"
MIN_SCORE = 3  # garde-fou : en dessous, on ne répond pas (voir README, "Garde-fous")


def normalize(text: str) -> list[str]:
    """Minuscules, suppression des accents, tokenisation simple."""
    text = unicodedata.normalize("NFD", text.lower())
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    # Les jetons d'une lettre ("t" de "reste-t-il") sont du bruit : écartés.
    return [t for t in re.findall(r"[a-z0-9]+", text) if len(t) > 1 or t.isdigit()]


STOPWORDS = set(normalize(
    "le la les de des du un une et est je tu il elle nous vous mon ma mes "
    "ce cette au aux en dans sur pour par pas que qui quoi combien temps"
))


def load_chunks() -> list[dict]:
    """Charge les documents et les découpe en sections (chunking par titre ##)."""
    chunks = []
    for path in sorted(KB_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        sections = re.split(r"\n## ", text)
        for section in sections:
            section = section.strip()
            if not section or section.startswith("# "):
                continue
            title, _, body = section.partition("\n")
            chunks.append({
                "source": path.name,
                "title": title.strip(),
                "text": body.strip(),
                "title_tokens": set(normalize(title)) - STOPWORDS,
                "body_tokens": set(normalize(body)) - STOPWORDS,
            })
    return chunks


def retrieve(question: str, chunks: list[dict]) -> tuple[dict | None, int]:
    """Retrouve le chunk le plus proche par recouvrement lexical.

    Le titre d'une section d'aide est rédigé comme la question à laquelle
    elle répond : ses mots comptent donc double par rapport au corps.
    """
    q_tokens = set(normalize(question)) - STOPWORDS
    best, best_score = None, 0
    for chunk in chunks:
        score = 2 * len(q_tokens & chunk["title_tokens"]) + len(q_tokens & chunk["body_tokens"])
        if score > best_score:
            best, best_score = chunk, score
    return best, best_score


def generate(question: str, chunk: dict | None, score: int) -> str:
    """Génération simulée : répond uniquement à partir du passage retrouvé."""
    if chunk is None or score < MIN_SCORE:
        return (
            "Je n'ai pas trouvé cette information dans la base d'aide. "
            "Un conseiller peut vous répondre — je ne préfère pas deviner."
        )
    return (
        f"D'après l'aide « {chunk['title']} » ({chunk['source']}) :\n\n"
        f"{chunk['text']}\n\n"
        "— Réponse construite uniquement à partir de la base de connaissances."
    )


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        return
    question = " ".join(sys.argv[1:])
    chunks = load_chunks()
    chunk, score = retrieve(question, chunks)
    print(f"Question : {question}")
    print(f"Chunks indexés : {len(chunks)} | meilleur score : {score}\n")
    print(generate(question, chunk, score))


if __name__ == "__main__":
    main()
