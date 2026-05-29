#!/usr/bin/env python3
import subprocess
import click

@click.group()
def cli():
    """🤖 Smart Warehouse System CLI Control Panel.
    Implemented by Munisa (Coordinator Squad).
    """
    pass

@cli.command()
@click.option('--record', is_flag=True, help='Trigger automated rosbag recording.')
def start(record):
    """[Task 14] Launches the master warehouse system setup."""
    click.echo(click.style("🚀 Initializing Master Launch Configuration...", fg='green', bold=True))
    subprocess.Popen(["roslaunch", "smart_warehouse_coordination", "main_system.launch"])
    
    if record:
        click.echo(click.style("🔴 ROSBAG RECORDING STARTED", fg='red', bold=True))
        subprocess.Popen(["rosbag", "record", "-A", "-O", "warehouse_mission.bag"])

@cli.command()
def test_system():
    """[Task 13] Interface loop to trigger Pytest validation."""
    click.echo("🧪 Initiating Pytest Quality Assurance Testing...")
    subprocess.run(["pytest", "tests/"])

if __name__ == '__main__':
    cli()