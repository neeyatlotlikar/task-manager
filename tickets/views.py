from django.shortcuts import render



def index(request):
    return render(
        request,
        "tickets/index.html",
        content_type="text/html",
        status=200,
    )
