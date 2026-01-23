from typing import Any

import logfire


def scrubbing_callback(match: logfire.ScrubMatch) -> Any:
    if "social_security_contribution" in match.path:
        return match.value

    return None
