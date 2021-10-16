#Python script to start and stop AWS EC2 instances using tags and defined times in the script itself and also in the AWS Cloudwatch rules 
#that must been created to use with this script in the AWS Lambda functions.


import boto3
import collections
import time
import datetime
import sys
from datetime import datetime

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    
	now = datetime.now()

	if now.hour == 10:

		stoppedInstances = ec2.describe_instances(
			Filters=[
				{'Name': 'tag:StartStop', 'Values': ['1','2']}, {'Name': 'instance-state-name', 'Values': ['stopped']}
			]
		).get(
			'Reservations', []
		)

		instancesStopped = sum(
			[
				[i for i in r['Instances']]
				for r in stoppedInstances
			], [])

		print("Found %d instances to start now:" % len(instancesStopped))

		#Lopping through all instances from filters
		for instance in instancesStopped:

			instanceName = [
					t.get('Value') for t in instance['Tags']
					if t['Key'] == 'Name'][0]

			#Checking if instances are stopped
			if instance["State"]["Name"] == "stopped":
				res = boto3.resource("ec2")
				startingUp = res.Instance(instance["InstanceId"])
				startingUp.start()

				print("Started the following instances: " + instanceName)

	if now.hour == 22:

		runningInstances = ec2.describe_instances(
			Filters=[
				{'Name': 'tag:StartStop', 'Values': ['1']}, {'Name': 'instance-state-name', 'Values': ['running']}
			]
		).get(
			'Reservations', []
		)

		instancesRunning = sum(
			[
				[i for i in r['Instances']]
				for r in runningInstances
			], [])

		print("Found %d instances to stop now:" % len(instancesRunning))

		#Lopping through all instances from filters
		for instance in instancesRunning:

			instanceName = [
					t.get('Value') for t in instance['Tags']
					if t['Key'] == 'Name'][0]

			#Checking if instances are running
			if instance["State"]["Name"] == "running":
				res = boto3.resource("ec2")
				shuttingDown = res.Instance(instance["InstanceId"])
				shuttingDown.stop()

				print("Stopped the following instances: " + instanceName)

	if now.hour == 2:

		runningInstances = ec2.describe_instances(
			Filters=[
				{'Name': 'tag:StartStop', 'Values': ['2']}, {'Name': 'instance-state-name', 'Values': ['running']}
			]
		).get(
			'Reservations', []
		)

		instancesRunning = sum(
			[
				[i for i in r['Instances']]
				for r in runningInstances
			], [])

		print("Found %d instances to stop now:" % len(instancesRunning))

		#Lopping through all instances from filters
		for instance in instancesRunning:

			instanceName = [
					t.get('Value') for t in instance['Tags']
					if t['Key'] == 'Name'][0]

			#Checking if instances are running
			if instance["State"]["Name"] == "running":
				res = boto3.resource("ec2")
				shuttingDown = res.Instance(instance["InstanceId"])
				shuttingDown.stop()

				print("Stopped the following instances: " + instanceName)

	if now.hour != 10 and now.hour != 22 and now.hour != 2:

		print("There is nothing to do at this time!")
        
	return "Done!"
