from logging import Filter

from .utils import get_client_ip


class IPAddressFilter(Filter):
    def filter(self, record):
        if hasattr(record, 'request'):
            record.ip = get_client_ip(request=record.request)
            record.method = record.request.method

        return True
