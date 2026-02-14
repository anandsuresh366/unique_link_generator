from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import ProtectedLink, Device
from .utils import get_fingerprint

def generate_link(request):
    if request.method=="POST":
        link=ProtectedLink.objects.create(
            original_url=request.POST.get("original_url"),
            device_limit=int(request.POST.get("device_limit"))
        )
        return render(request,"index.html",{"protected_url":request.build_absolute_uri(f"/go/{link.token}/")})
    return render(request,"index.html")

def protected_view(request,token):
    link=get_object_or_404(ProtectedLink,token=token)
    fp=get_fingerprint(request)
    if Device.objects.filter(link=link,fingerprint=fp).exists():
        return redirect(link.original_url)
    if Device.objects.filter(link=link).count()>=link.device_limit:
        return HttpResponseForbidden("DEVICE LIMIT REACHED")
    Device.objects.create(link=link,fingerprint=fp)
    return redirect(link.original_url)
