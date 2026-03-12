import hashlib

def get_fingerprint(request):

    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR", "")

    user_agent = request.META.get("HTTP_USER_AGENT", "")
    language = request.META.get("HTTP_ACCEPT_LANGUAGE", "")

    raw_string = f"{ip}|{user_agent}|{language}"

    return hashlib.sha256(raw_string.encode("utf-8")).hexdigest()