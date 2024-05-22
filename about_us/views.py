from django.shortcuts import render
from accounts.models import User


def about_us(request):
    full_names = [user.get_full_name().strip() for user in User.objects.all()]
    return render(request, "about_us.html", context={"full_names": full_names})
