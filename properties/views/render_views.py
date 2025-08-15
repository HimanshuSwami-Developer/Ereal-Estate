from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.template import TemplateDoesNotExist

class RenderHTMLPages:
    def __call__(self, request, page_name="base"):  # Default to "base" if no page_name provided
        # Ignore browser's favicon request
        if page_name == "favicon.ico":
            return HttpResponseNotFound("Favicon not found")

        try:
            return render(request, f"{page_name}.html")
        except TemplateDoesNotExist:
            return HttpResponseNotFound("Page not found")