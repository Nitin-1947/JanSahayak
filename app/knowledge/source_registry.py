OFFICIAL_SOURCES = {

    "myscheme":
        "https://www.myscheme.gov.in/",

    "uidai":
        "https://uidai.gov.in/",

    "my_aadhaar":
        "https://myaadhaar.uidai.gov.in/",
}


def get_source(name: str):

    return OFFICIAL_SOURCES.get(name)