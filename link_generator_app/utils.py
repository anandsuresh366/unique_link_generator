import uuid

def get_fingerprint(request):
    fingerprint = request.COOKIES.get("device_fp")

    if not fingerprint:
        fingerprint = str(uuid.uuid4())

    return fingerprint