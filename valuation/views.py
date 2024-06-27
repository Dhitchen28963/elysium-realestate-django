from django.shortcuts import render

def valuation_view(request):
    return render(request, 'valuation/valuation.html')