def get_client_ip(request) -> str:
    x_forwarded_for = request.META.get('HTTP_REMOTE_ADDR')

    return (x_forwarded_for.split(',')[0] if x_forwarded_for else
            request.META.get('REMOTE_ADDR'))


def get_logger_extra(request) -> dict[str, str]:
    return dict(
        ip=get_client_ip(request=request),
        method=request.method
    )
