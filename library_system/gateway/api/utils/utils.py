import re


def get_http_headers(request):
    regex = re.compile("^HTTP_")
    result = dict(
        (regex.sub("", header), value)
        for (header, value) in request.META.items()
        if header.startswith("HTTP_")
    )

    return result
