"""
Pytest scenarios for package verification system.
"""


def verify_package(package_name):

    if package_name == "Blue Box":
        return f"Package Verified: {package_name}"

    return f"Package Rejected: {package_name}"


def test_valid_package():

    result = verify_package("Blue Box")

    assert result == "Package Verified: Blue Box"


def test_invalid_package():

    result = verify_package("Red Box")

    assert result == "Package Rejected: Red Box"