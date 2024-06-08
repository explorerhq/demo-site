from django.contrib.auth import authenticate, login

from django.utils.deprecation import MiddlewareMixin
from django.template.loader import render_to_string



class AutoLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not request.path.startswith('/admin/'):
            user = authenticate(username='admin', password='admin')
            if user is not None:
                login(request, user)
        response = self.get_response(request)
        return response



class HeaderInjectionMiddleware(MiddlewareMixin):
    def process_response(self, request, response):

        # Don't inject into schema frame
        if 'text/html' in response['Content-Type'] and b'value="explorer_schema"' not in response.content:
            header_html = render_to_string('header.html')
            body_start_index = response.content.find(b'<body>')
            if body_start_index != -1:
                response.content = (
                    response.content[:body_start_index] +
                    header_html.encode('utf-8') +
                    response.content[body_start_index:]
                )
        return response
