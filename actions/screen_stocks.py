from actions.mock_screener import screen_stocks as mock_screen


def screen_stocks(ctx) -> list[str]:
    """Screen stocks using config screening params and current date."""
    return mock_screen(ctx.processing_date, ctx.config.screening)
