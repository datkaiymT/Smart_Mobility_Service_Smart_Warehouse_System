"""
Communication flow tests.
"""


def mission_status(message):

    if "Verified" in message:
        return "Mission Complete"

    return "Mission Failed"


def test_successful_mission():

    result = mission_status("Package Verified: Blue Box")

    assert result == "Mission Complete"


def test_failed_mission():

    result = mission_status("Package Rejected: Red Box")

    assert result == "Mission Failed"