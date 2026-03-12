import uuid

def get_fingerprint(request):
    """
    Returns a stable device fingerprint.
    If the device has no cookie yet, generate a new UUID.
    """

    fingerprint = request.COOKIES.get("device_fp")

    if not fingerprint:
        fingerprint = str(uuid.uuid4())

    return fingerprint