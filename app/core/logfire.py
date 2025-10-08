from typing import Any

import logfire


def scrubbing_callback(match: logfire.ScrubMatch) -> Any:
    if match.path == ("attributes", "article", "social_security_levy"):
        return match.value

    return None
