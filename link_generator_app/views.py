import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.conf import settings
from django.db import transaction
from django.urls import reverse

from .models import ProtectedLink, Device
from .forms import LinkForm
from .utils import get_fingerprint


def generate_link(request):

    if request.method == "POST":
        form = LinkForm(request.POST)

        if form.is_valid():
            original_url = form.cleaned_data["original_url"]
            device_limit = form.cleaned_data["device_limit"]

            link = ProtectedLink.objects.create(
                original_url=original_url,
                device_limit=device_limit
            )

            protected_url = request.build_absolute_uri(
                reverse("protected", args=[link.token])
            )

            return render(request, "index.html", {
                "protected_url": protected_url,
                "form": form
            })

    else:
        form = LinkForm()

    return render(request, "index.html", {"form": form})


def protected_view(request, token):

    link = get_object_or_404(ProtectedLink, token=token)

    fingerprint = get_fingerprint(request)

    with transaction.atomic():

        device_exists = Device.objects.filter(
            link=link,
            fingerprint=fingerprint
        ).exists()

        if not device_exists:

            if Device.objects.filter(link=link).count() >= link.device_limit:
                return HttpResponseForbidden("""
                    <h1 style="color:red;text-align:center;margin-top:20%;">
                        DEVICE LIMIT REACHED
                    </h1>
                """)

            Device.objects.create(
                link=link,
                fingerprint=fingerprint
            )

    return redirect(link.original_url)