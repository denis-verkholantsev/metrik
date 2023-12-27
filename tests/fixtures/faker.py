from datetime import datetime

import pytest


@pytest.fixture(autouse=True)
def faker_seed() -> int:
    now = datetime.utcnow()
    return (
        now.second
        + now.minute * 100
        + now.hour * 10_000
        + now.day * 1000_000
        + now.month * 100_000_000
        + now.year * 10_000_000_000
    )
