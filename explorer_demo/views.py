from django.http import HttpResponse


def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /play/",
        "Disallow: /logs/",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
