import re
from datetime import date, timedelta

from dateutil.relativedelta import relativedelta


def advance(ctx) -> bool:
    """Advance processing_date by interval. Return False if past end boundary."""
    if ctx.processing_date is None:
        ctx.processing_date = ctx.config.start_date
        return True

    next_date = _next_date(ctx.processing_date, ctx.config.interval)
    if next_date > ctx.config.end_date:
        return False

    ctx.processing_date = next_date
    return True


def _next_date(current: date, interval: str) -> date:
    """Calculate next date based on interval string."""
    if interval == "day":
        return current + timedelta(days=1)
    elif interval == "month":
        return current + relativedelta(months=1)
    else:
        match = re.match(r"^(\d+)days$", interval)
        if match:
            n = int(match.group(1))
            return current + timedelta(days=n)
        raise ValueError(f"Unknown interval: {interval}")
