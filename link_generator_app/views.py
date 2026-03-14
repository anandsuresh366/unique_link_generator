import uuid

from django.db import transaction
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse

from link_generator_app.forms import LinkForm
from link_generator_app.models import Device, ProtectedLink


# ---------------------------
# LINK GENERATION
# ---------------------------
def generate_link(request):

    protected_url = None

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

    else:
        form = LinkForm()

    return render(request, "index.html", {
        "form": form,
        "protected_url": protected_url
    })


# ---------------------------
# PROTECTED LINK VIEW
# ---------------------------
def protected_view(request, token):

    link = get_object_or_404(ProtectedLink, token=token)

    device_id = request.COOKIES.get("device_id")

    # Create fingerprint if first visit
    if not device_id:
        device_id = str(uuid.uuid4())

    with transaction.atomic():

        # Check if this device already registered
        device_exists = Device.objects.filter(
            link=link,
            fingerprint=device_id
        ).exists()

        # If new device, verify limit
        if not device_exists:

            device_count = Device.objects.filter(link=link).count()

            # Limit check (accurate)
            if device_count >= link.device_limit:
                return render(request, "limit.html", status=403)

            # Register new device
            Device.objects.create(
                link=link,
                fingerprint=device_id
            )

    response = redirect(link.original_url)

    # Save device cookie
    response.set_cookie(
        "device_id",
        device_id,
        max_age=60 * 60 * 24 * 365,
        httponly=True,
        samesite="Lax"
    )

    return response