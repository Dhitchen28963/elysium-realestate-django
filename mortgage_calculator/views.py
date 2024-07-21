from django.shortcuts import render


def mortgage_calculator_view(request):
    return render(request, 'mortgage_calculator/mortgage_calculator.html')
