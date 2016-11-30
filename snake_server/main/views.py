from django.shortcuts import render, render_to_response


# Create your views here.

def controller(request):
    return render_to_response('controller.html')
