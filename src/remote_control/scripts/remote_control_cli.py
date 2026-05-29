#!/usr/bin/env python3
"""
Smart Mobility Systems Engineering - Smart Warehouse Project
Author: [Your Name]
Function 4: Advanced CLI Command Interface (Click Library)
"""

import click
import rospy
from geometry_msgs.msg import Twist

def stream_velocity(linear_x, duration=1.0):
    """Helper function to cleanly connect to ROS and stream a velocity command."""
    try:
        # Initialize node anonymously
        rospy.init_node('remote_control_cli_node', anonymous=True, disable_signals=True)
        pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        
        # Give ROS a brief moment to hook up to the network connections
        rospy.sleep(0.3)
        
        if rospy.is_shutdown():
            return False
            
        # Construct the kinematic Twist message
        move_cmd = Twist()
        move_cmd.linear.x = float(linear_x)
        move_cmd.linear.y = 0.0
        move_cmd.linear.z = 0.0
        move_cmd.angular.x = 0.0
        move_cmd.angular.y = 0.0
        move_cmd.angular.z = 0.0
        
        # Continuously stream the command at 10Hz over the specified duration
        rate = rospy.Rate(10)
        cycles = int(duration * 10)
        
        for _ in range(cycles):
            if rospy.is_shutdown():
                break
            pub.publish(move_cmd)
            rate.sleep()
            
        return True
    except Exception:
        return False

@click.group()
def cli():
    """🤖 Warehouse Mobile Platform Remote Control CLI Panel"""
    pass

@cli.command()
@click.option('--speed', default=0.2, help='Linear forward speed in m/s (default: 0.2)')
def forward(speed):
    """🚀 Drive the warehouse robot forward at a specified velocity."""
    click.echo(click.style(f"📥 Handshaking with ROS... Streaming Forward Vector at {speed} m/s...", fg="green"))
    
    success = stream_velocity(linear_x=speed)
    
    if success:
        click.echo(click.style("✅ Transmission complete. Command locked into simulator runtime.", fg="cyan"))
    else:
        click.echo(click.style("❌ ROS Master is not running! Ensure your background simulation is active.", fg="red"))

@cli.command()
def halt():
    """🛑 Emergency Stop: Instantly halt all platform motors."""
    click.echo(click.style("🚨 EMERGENCY HALT REQUESTED!", fg="yellow", bold=True))
    
    success = stream_velocity(linear_x=0.0, duration=0.5)
    
    if success:
        click.echo(click.style("🛑 All velocity vectors successfully zeroed out.", fg="red", bold=True))
    else:
        click.echo(click.style("❌ ROS Transmission Failure.", fg="red"))

if __name__ == '__main__':
    cli()
