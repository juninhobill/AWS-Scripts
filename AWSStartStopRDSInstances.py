#Python script to start and stop AWS RDS instances using tags and defined times in the script itself and also in the AWS Cloudwatch 
#rules that must been created to use with this script in the AWS Lambda functions.


import boto3
import collections
import time
import datetime
import sys
from datetime import datetime

rds = boto3.client('rds')

def lambda_handler(event, context):

	print("Check RDS's tags and current time")
	
	#Getting current time
	now = datetime.now()
	current_time = time.strftime("%H:%M")

	#Search all the instances which contains scheduled filter 
	instances = rds.describe_db_instances()

	stopInstances = []
	startInstances = []

	if now.hour == 22:

		for instance in instances["DBInstances"]:
			tags = rds.list_tags_for_resource(ResourceName=instance["DBInstanceArn"])
			status = instance['DBInstanceStatus']
			for tag in tags["TagList"]:
				if tag['Key'] == 'StartStop':
					if tag['Value'] == '2':
						if status == 'available':
							stopInstances.append(instance["DBInstanceIdentifier"])
							rds.stop_db_instance(DBInstanceIdentifier=instance["DBInstanceIdentifier"])   
							pass
						pass
					pass
				pass
			pass
		pass
	
	if now.hour == 2:

		for instance in instances["DBInstances"]:
			tags = rds.list_tags_for_resource(ResourceName=instance["DBInstanceArn"])
			status = instance['DBInstanceStatus']
			for tag in tags["TagList"]:
				if tag['Key'] == 'StartStop':
					if tag['Value'] == '1':
						if status == 'available':
							stopInstances.append(instance["DBInstanceIdentifier"])
							rds.stop_db_instance(DBInstanceIdentifier=instance["DBInstanceIdentifier"])   
							pass
						pass
					pass
				pass
			pass
		pass


	if now.hour == 9:

		for instance in instances["DBInstances"]:
			tags = rds.list_tags_for_resource(ResourceName=instance["DBInstanceArn"])
			status = instance['DBInstanceStatus']
			for tag in tags["TagList"]:
				if tag['Key'] == 'StartStop':
					if tag['Value'] == '1':
						if status == 'stopped':
							startInstances.append(instance["DBInstanceIdentifier"])
							rds.start_db_instance(DBInstanceIdentifier=instance["DBInstanceIdentifier"])
							pass
						pass
					pass
				pass
			pass
		pass

	print(current_time)

	if now.hour == 22:
	
		#Shutdown all instances tagged to stop. 
		if len(stopInstances) > 0:
			print("Stopping the following RDS instances: ", stopInstances)
		else:
			print("No RDS instances to be shutdown now.")

	if now.hour == 2:
	
		#Shutdown all instances tagged to stop. 
		if len(stopInstances) > 0:
			print("Stopping the following RDS instances: ", stopInstances)
		else:
			print("No RDS instances to be shutdown now.")
			
	if now.hour == 9:


		#Started all instances tagged to stop. 
		if len(startInstances) > 0:
			print("Starting the following RDS instances: ", startInstances)
		else:
			print("No RDS instances to be started now.")
		
	if now.hour != 9 and now.hour != 22 and now.hour != 2:
	
		print("There is nothing to do at this time!")

	return "Done!"
