import hashlib

def get_fingerprint(request):
    ip = request.META.get("HTTP_X_FORWARDED_FOR","").split(",")[0] or request.META.get("REMOTE_ADDR","")
    ua = request.META.get("HTTP_USER_AGENT","")
    lang = request.META.get("HTTP_ACCEPT_LANGUAGE","")
    return hashlib.sha256(f"{ua}|{ip}|{lang}".encode()).hexdigest()
