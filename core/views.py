from django.shortcuts import render

from .models import SubscriptionPlan


# Create your views here.

def home(request):

    subscriptionplans = SubscriptionPlan.objects.all()

    context = {'subscriptionplans': subscriptionplans}
    return render(request, 'core/home.html', context)
