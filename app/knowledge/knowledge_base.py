import json
from pathlib import Path


class KnowledgeBase:

    def __init__(self, directory: Path):
        self.directory = directory

    def load_all(self):

        documents = []

        for file in self.directory.glob("*.json"):

            with open(
                file,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

            if isinstance(data, list):
                documents.extend(data)
            else:
                documents.append(data)

        return documents

    def search(self, query: str):

        query_words = set(
            query.lower().split()
        )

        results = []

        for document in self.load_all():

            text = (
                document.get("title", "")
                + " "
                + document.get("question", "")
                + " "
                + document.get("answer", "")
            ).lower()

            score = sum(
                word in text
                for word in query_words
            )

            if score > 0:
                results.append(
                    (score, document)
                )

        results.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return [
            document
            for _, document in results[:5]
        ]