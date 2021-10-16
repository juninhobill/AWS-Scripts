#Automated AMI Backups on AWS Lambda for EC2 instances

#This script will search for all instances having a tag with "Backup" or "backup" on it. As soon as we have the instances list, 
#we loop through each instance and create an AMI of it. Also, it will look for a "Retention" tag key which will be used as a 
#retention policy number in days. If there is no tag with that name, it will use a 7 days default value for each AMI. After 
#creating the AMI it creates a "DeleteOn" tag on the AMI indicating when it will be deleted using the Retention value and another 
#Lambda function called "AWSlambdaAMICleanup".


import boto3
import collections
import datetime
import sys
import pprint

ec = boto3.client('ec2')

def lambda_handler(event, context):

	reservations = ec.describe_instances(
		Filters=[
			{'Name': 'tag-key', 'Values': ['backup', 'Backup']},
		]
	).get(
		'Reservations', []
	)

	instances = sum(
		[
			[i for i in r['Instances']]
			for r in reservations
		], [])

	print ("Found %d instances that need backing up" % len(instances))

	to_tag = collections.defaultdict(list)
	inDone = []

	for instance in instances:
		try:
			retention_days = [
				int(t.get('Value')) for t in instance['Tags']
				if t['Key'] == 'Retention'][0]
		except IndexError:
			retention_days = 5

		finally:

			create_time = datetime.datetime.now().date()
			create_fmt = create_time.strftime('%Y-%m-%d')

			if str(instance['InstanceId']) not in inDone:

				name_Tag = "".join([str(t.get('Value')) for t in instance['Tags']
				if t['Key'] == 'Name'])

				AMIid = ec.create_image(InstanceId=instance['InstanceId'], Name="BKP - " + name_Tag + " - " + create_fmt, Description="Lambda created AMI of instance " + instance['InstanceId'] + " from " + create_fmt, NoReboot=True, DryRun=False)

				inDone.insert(0,str(instance['InstanceId']))

				ec.create_tags(
				Resources=[AMIid['ImageId']],
				Tags=[
				{'Key': 'Name', 'Value': name_Tag}
			]
		)

				print ("Created AMI %s of instance %s " % (AMIid['ImageId'], instance['InstanceId']))

			else:

				print ("We already got an AMI of instance %s " % (instance['InstanceId']))

			pprint.pprint(instance)

			to_tag[retention_days].append(AMIid['ImageId'])

			print ("Retaining AMI %s of instance %s for %d days" % (
				AMIid['ImageId'],
				instance['InstanceId'],
				retention_days,
			))

	for retention_days in to_tag.keys():
		delete_date = datetime.date.today() + datetime.timedelta(days=retention_days)
		delete_fmt = delete_date.strftime('%m-%d-%Y')

		print ("Will delete %d AMIs on %s" % (len(to_tag[retention_days]), delete_fmt))

		ec.create_tags(
			Resources=to_tag[retention_days],
			Tags=[
				{'Key': 'DeleteOn', 'Value': delete_fmt}
			]
		)

	return "Done!"
