# =============================================================================
# test_status_reporting.py
# -----------------------------------------------------------------------------
# Pytest scenarios for Slot #6 -- Status Reporting.
# These tests validate the pure logic (parsing, formatting, state changes)
# WITHOUT requiring a live roscore. This is the same approach Datkaiym used
# for the eco_router pytest, keeping our package style consistent.
#
# Run with:   pytest -v test_status_reporting.py
# =============================================================================

import pytest


# -----------------------------------------------------------------------------
# Helper functions extracted from the node logic so they can be tested
# without spinning up ROS. (In a real ROS package these would live in a shared
# module imported by both the node and the tests.)
# -----------------------------------------------------------------------------
def parse_detection(raw):
    """Parse a 'label,confidence,x,y' string -- returns dict or None."""
    try:
        parts = raw.split(",")
        return {
            "label": parts[0].strip(),
            "confidence": float(parts[1]),
            "x": float(parts[2]),
            "y": float(parts[3]),
        }
    except (IndexError, ValueError):
        return None


def format_log_line(elapsed, wallclock, speed, target, comm, slam_conf):
    """Format a single mission log line (mirrors MissionLogger.publish_log)."""
    return (
        f"[T+{elapsed:6.1f}s | {wallclock}] "
        f"speed={speed:+.2f} m/s | "
        f"target={target} | "
        f"comm={comm} | "
        f"slam_conf={slam_conf:.2f}"
    )


# -----------------------------------------------------------------------------
# TARGET TRACKER TESTS
# -----------------------------------------------------------------------------
class TestTargetTracker:
    """Tests for the detection parsing logic in Function 1."""

    def test_valid_detection_parses_correctly(self):
        """A well-formed detection string should parse into all fields."""
        result = parse_detection("BlueBox,0.87,2.3,1.1")
        assert result is not None
        assert result["label"] == "BlueBox"
        assert result["confidence"] == pytest.approx(0.87)
        assert result["x"] == pytest.approx(2.3)
        assert result["y"] == pytest.approx(1.1)

    def test_malformed_detection_returns_none(self):
        """Missing fields must not crash the node -- they return None."""
        assert parse_detection("BlueBox,0.87") is None
        assert parse_detection("garbage_input") is None
        assert parse_detection("") is None

    def test_whitespace_in_label_is_stripped(self):
        """Labels with leading/trailing spaces should be cleaned."""
        result = parse_detection("  RedBox  ,0.5,1.0,2.0")
        assert result["label"] == "RedBox"


# -----------------------------------------------------------------------------
# MISSION LOG TESTS
# -----------------------------------------------------------------------------
class TestMissionLog:
    """Tests for the log line formatting in Function 2."""

    def test_log_line_contains_all_fields(self):
        """Every field passed in must show up in the output string."""
        line = format_log_line(
            elapsed=12.3,
            wallclock="14:25:01",
            speed=0.40,
            target="BlueBox",
            comm="OK",
            slam_conf=0.85,
        )
        assert "T+  12.3s" in line
        assert "14:25:01" in line
        assert "+0.40 m/s" in line
        assert "BlueBox" in line
        assert "comm=OK" in line
        assert "slam_conf=0.85" in line

    def test_negative_velocity_renders_with_sign(self):
        """Reverse motion must be represented with an explicit minus sign."""
        line = format_log_line(1.0, "00:00:01", -0.25, "NONE", "OK", 0.5)
        assert "-0.25 m/s" in line

    def test_unknown_defaults_render(self):
        """Before any teammate node is alive, defaults must still format cleanly."""
        line = format_log_line(0.0, "00:00:00", 0.0, "NONE", "UNKNOWN", 0.0)
        assert "target=NONE" in line
        assert "comm=UNKNOWN" in line
        assert "slam_conf=0.00" in line
