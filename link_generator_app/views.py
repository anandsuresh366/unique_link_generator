import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponse
from django.conf import settings
from .models import ProtectedLink, Device
from .utils import get_fingerprint

def generate_link(request):


    if request.method == "POST":
        original_url = request.POST.get("original_url")
        device_limit = int(request.POST.get("device_limit"))

        link = ProtectedLink.objects.create(
            original_url=original_url,
            device_limit=device_limit
        )

        base_url = getattr(settings, "BASE_URL", request.build_absolute_uri("/").rstrip("/"))
        protected_url = f"{base_url}/go/{link.token}/"

        return render(request, "index.html", {"protected_url": protected_url})

    return render(request, "index.html")


import uuid
from django.db import IntegrityError

import uuid
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.db import transaction

def protected_view(request, token):
    link = get_object_or_404(ProtectedLink, token=token)

    # Get or create stable device ID cookie
    device_id = request.COOKIES.get("device_id")
    if not device_id:
        device_id = str(uuid.uuid4())

    with transaction.atomic():
        # Check if this device already registered
        device_exists = Device.objects.filter(
            link=link,
            fingerprint=device_id
        ).exists()

        if not device_exists:
            current_devices = Device.objects.filter(link=link).count()

            if current_devices >= link.device_limit:
                return HttpResponseForbidden("""
                    <h1 style="color:red;text-align:center;margin-top:20%;">
                        DEVICE LIMIT REACHED
                    </h1>
                """)

            Device.objects.create(
                link=link,
                fingerprint=device_id
            )

    response = redirect(link.original_url)
    response.set_cookie("device_id", device_id, max_age=60*60*24*365)
    return response



