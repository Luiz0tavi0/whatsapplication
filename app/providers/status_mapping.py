ZAPI_STATUS_MAP = {
    'SENT': 'sent',
    'DELIVERED': 'received',
    'READ': 'read',
    'FAILED': 'failed',
}

WIREWEB_STATUS_MAP = {
    'message.sent': 'sent',
    'message.delivered': 'received',
    'message.read': 'read',
    'message.failed': 'failed',
}

STATUS_MAPS = {
    'zapi': ZAPI_STATUS_MAP,
    'wireweb': WIREWEB_STATUS_MAP,
}


def normalize_status(provider: str, raw_status: str) -> str | None:
    mapping = STATUS_MAPS.get(provider, {})
    return mapping.get(raw_status)
