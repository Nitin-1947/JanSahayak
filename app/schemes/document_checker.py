class DocumentChecker:

    def check_documents(
        self,
        scheme,
        available_documents: list[str]
    ):

        required = set(
            document.lower()
            for document in scheme.documents
        )

        available = set(
            document.lower()
            for document in available_documents
        )

        missing = sorted(
            required - available
        )

        return {
            "required": sorted(required),
            "available": sorted(available),
            "missing": missing,
            "complete": len(missing) == 0
        }