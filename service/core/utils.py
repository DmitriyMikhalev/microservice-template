def get_client_ip(request) -> str:
    return request.META.get('HTTP_X_REAL_IP')


def get_logger_extra(request) -> dict[str, str]:
    return dict(
        ip=get_client_ip(request=request),
        method=request.method
    )
