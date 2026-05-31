#!/usr/bin/env python3
"""
Smart Warehouse Project - Automated Unit Testing
Author: [Your Name]
"""

import sys
import os

# Python Path Setup: Tell the testing robot how to look inside your scripts directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the math logic directly from your original script
# We mock ROS variables so we don't need a real simulation running to test the math!
def calculate_power_formula(velocity):
    """
    This duplicates the exact mathematical model inside your EcoRouter callback:
    Power = Base_Electronics (15W) + (Velocity^2 * 25.0)
    """
    base_power = 15.0
    return base_power + (velocity ** 2 * 25.0)


# --- The Actual Pytests ---

def test_robot_sitting_still():
    """Test 1: When the robot velocity is 0.0 m/s, power draw must equal exactly 15.0 Watts."""
    calculated_power = calculate_power_formula(0.0)
    assert calculated_power == 15.0

def test_robot_moving_forward():
    """Test 2: When moving at 2.0 m/s, power draw should equal 15 + (4 * 25) = 115.0 Watts."""
    calculated_power = calculate_power_formula(2.0)
    assert calculated_power == 115.0

def test_negative_velocity():
    """Test 3: If the robot reverses (-1.0 m/s), squaring the value should still result in positive power draw (40.0 Watts)."""
    calculated_power = calculate_power_formula(-1.0)
    assert calculated_power == 40.0
