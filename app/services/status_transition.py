STATUS_ORDER = {
    "pending": 0,
    "sent": 1,
    "received": 2,
    "read": 3,
}

TERMINAL_FAILURE = "failed"


def is_valid_transition(current: str, new: str) -> bool:
    if new == TERMINAL_FAILURE:
        # só falha se ainda não confirmou entrega/leitura
        return current not in {"received", "read"}

    if current == TERMINAL_FAILURE:
        # depois de failed, não aceita reabrir pra sent/received/read
        return False

    current_rank = STATUS_ORDER.get(current, -1)
    new_rank = STATUS_ORDER.get(new, -1)
    return new_rank > current_rank
