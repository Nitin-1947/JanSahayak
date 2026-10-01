class ApplicationGuide:

    def get_guide(self, scheme):

        return {
            "scheme_name": scheme.name,

            "benefits": scheme.benefits,

            "documents": scheme.documents,

            "steps": scheme.application_steps,

            "application_url":
                scheme.application_url,

            "official_source":
                scheme.official_source_url,

            "last_verified":
                scheme.last_verified,
        }