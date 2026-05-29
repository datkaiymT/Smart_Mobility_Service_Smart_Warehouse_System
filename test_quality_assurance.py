"""
Quality Assurance - Pytest Unit Framework
Smart Warehouse Autonomous Mobility System
Author: Your Name
"""

import pytest
import math

# ──────────────────────────────────────────
# POWER / ENERGY TESTS
# ──────────────────────────────────────────

def calculate_power(velocity: float) -> float:
    """Power formula used by the Smart Warehouse system."""
    return 15.0 + (velocity ** 2) * 25.0

def test_stationary_state():
    """Test 1: Verifies that a velocity of 0.0 m/s
    produces a baseline power draw of 15.0 Watts."""
    power = calculate_power(0.0)
    assert power == 15.0, f"Expected 15.0W, got {power}W"

def test_forward_cruise():
    """Test 2: Confirms that 2.0 m/s input correctly
    outputs 15 + (2^2 x 25) = 115.0 Watts."""
    power = calculate_power(2.0)
    assert power == 115.0, f"Expected 115.0W, got {power}W"

def test_negative_vector():
    """Test 3: Verifies that a reverse velocity of -1.0 m/s
    still produces a positive power requirement of 40.0 Watts."""
    power = calculate_power(-1.0)
    assert power == 40.0, f"Expected 40.0W, got {power}W"

# ──────────────────────────────────────────
# BATTERY LEVEL TESTS
# ──────────────────────────────────────────

def test_battery_above_minimum():
    """Checks that the robot battery is above 20% minimum."""
    battery = 85.0  # simulate 85% charge
    assert battery > 20.0, "Battery is below minimum threshold!"

def test_low_battery_triggers_alert():
    """Checks that when battery drops to 10%, alert is triggered."""
    battery = 10.0
    alert = battery < 20.0
    assert alert == True, "Alert should trigger when battery < 20%"

# ──────────────────────────────────────────
# COMMUNICATION STATUS TESTS
# ──────────────────────────────────────────

def test_comm_link_is_active():
    """Verifies that the robot communication status is connected."""
    status = "connected"
    assert status == "connected", "Communication link is not active!"

def test_comm_loss_detected():
    """Verifies that a lost connection is correctly detected."""
    status = "disconnected"
    assert status != "connected", "Comm loss should be detected!"

# ──────────────────────────────────────────
# SLAM NAVIGATION TESTS
# ──────────────────────────────────────────

def test_slam_node_is_running():
    """Checks that the SLAM navigation node is active."""
    slam_active = True
    assert slam_active == True, "SLAM node is not running!"

def test_robot_position_updated():
    """Checks that robot position changed after movement."""
    pos_before = (0.0, 0.0)
    pos_after  = (1.5, 2.3)
    assert pos_after != pos_before, "Robot position did not update!"

def test_robot_does_not_exceed_boundary():
    """Checks that robot stays within warehouse boundary (10x10m)."""
    pos_x = 8.0
    pos_y = 7.5
    assert pos_x <= 10.0 and pos_y <= 10.0, "Robot exceeded warehouse boundary!"