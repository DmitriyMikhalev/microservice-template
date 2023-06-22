def get_client_ip(request) -> str:
    x_forwarded_for = request.META.get('HTTP_REMOTE_ADDR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def get_logger_extra(request) -> dict[str, str]:
    return dict(
        ip=get_client_ip(request=request),
        method=request.method
    )
