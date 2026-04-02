from django.shortcuts import render

def home(request):
    message = None

    if request.method == "POST":
        url = request.POST.get("url")
        if url:
            message = "Download started successfully!"
        else:
            message = "Please enter a valid URL"

    return render(request, "core/index.html", {"message": message})

# Create your views here.
