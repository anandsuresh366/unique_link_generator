import uuid

from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from link_generator_app.forms import LinkForm
from link_generator_app.models import Device, ProtectedLink
from link_generator_app.utils import get_fingerprint


def generate_link(request):

    protected_url = None

    if request.method == "POST":
        form = LinkForm(request.POST)

        if form.is_valid():
            original_url = form.cleaned_data["original_url"]
            device_limit = form.cleaned_data["device_limit"]

            # internally store limit + 1
            link = ProtectedLink.objects.create(
                original_url=original_url,
                device_limit=device_limit + 1
            )

            protected_url = request.build_absolute_uri(
                reverse("protected", args=[link.token])
            )

    else:
        form = LinkForm()

    return render(request, "index.html", {
        "form": form,
        "protected_url": protected_url
    })

def protected_view(request, token):

    # 🔹 Ignore browser favicon request
    if request.path.endswith("favicon.ico"):
        return redirect("/")

    link = get_object_or_404(ProtectedLink, token=token)

    fingerprint = get_fingerprint(request)

    with transaction.atomic():

        device_exists = Device.objects.filter(
            link=link,
            fingerprint=fingerprint
        ).exists()

        if not device_exists:

            device_count = Device.objects.filter(link=link).count()

            if device_count >= link.device_limit:
                return render(request, "limit.html", status=403)

            Device.objects.create(
                link=link,
                fingerprint=fingerprint
            )

    response = redirect(link.original_url)

    response.set_cookie(
        "device_fp",
        fingerprint,
        max_age=60*60*24*365,
        httponly=True,
        samesite="Lax"
    )

    return response