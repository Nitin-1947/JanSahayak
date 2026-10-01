class FAQService:

    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base

    def answer(self, query: str):

        results = self.knowledge_base.search(
            query
        )

        if not results:
            return None

        return results[0]