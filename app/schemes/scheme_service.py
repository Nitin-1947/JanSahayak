class SchemeService:

    def __init__(self, matcher):
        self.matcher = matcher

    def get_user_schemes(
        self,
        profile
    ):

        results = self.matcher.find_matches(
            profile
        )

        return results

    def format_results(
        self,
        results
    ):

        formatted = []

        for result in results:

            formatted.append(
                {
                    "scheme_id":
                        result.scheme.scheme_id,

                    "name":
                        result.scheme.name,

                    "level":
                        result.scheme.level,

                    "state":
                        result.scheme.state,

                    "status":
                        result.status,

                    "benefits":
                        result.scheme.benefits,

                    "reasons":
                        result.reasons,

                    "missing":
                        result.missing,

                    "documents":
                        result.scheme.documents,

                    "application_steps":
                        result.scheme.application_steps,

                    "application_url":
                        result.scheme.application_url,

                    "official_source_url":
                        result.scheme.official_source_url,

                    "last_verified":
                        result.scheme.last_verified,
                }
            )

        return formatted