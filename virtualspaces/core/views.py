from django.shortcuts import render


def into_view(request):
    return render(request, 'core/intro.html')
