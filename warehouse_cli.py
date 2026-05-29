#!/usr/bin/env python3
import click
import rospy
from cli_manager.msg import RobotStatus  # Import your custom message

@click.group()
def cli():
    """Smart Warehouse Coordination System - Command Center"""
    pass

@cli.command()
def status():
    """Check the status of the warehouse system"""
    # Initialize node
    rospy.init_node('cli_listener', anonymous=True)
    
    click.echo("Connecting to warehouse system...")
    
    try:
        # Wait for one message from the 'robot_status' topic
        data = rospy.wait_for_message('robot_status', RobotStatus, timeout=5)
        
        click.echo("========================================")
        click.echo(f"  Robot ID: {data.robot_id}")
        click.echo(f"  Battery: {data.battery_level}%")
        click.echo(f"  Task: {data.current_task}")
        click.echo("========================================")
        
    except rospy.ROSException:
        click.echo("Error: Could not connect to robot. Is the publisher running?")

if __name__ == '__main__':
    cli()