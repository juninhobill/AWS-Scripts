#Python script to generate a pre-signed URL to upload files to an S3 bucket on AWS account.
#Edit the py file and fill out the following parameters:
#aws_access_key_id = 'Your AWS Access Key ID'
#aws_secret_access_key = 'Your AWS Access Key'
#Bucket = 'Your AWS S3 Bucket'
#Key = 'The name of the file to be uploaded'
#Other parameters like content-length-range and expires-in can also be edited.
#After that, just run the py file and the command CURL with the URL will be generated for you.


import boto3

s3 = boto3.client('s3',
	endpoint_url = 'https://s3.amazonaws.com',
	aws_access_key_id = '',
	aws_secret_access_key = '')

response = s3.generate_presigned_post(
	Bucket='',
	Key='',
	Conditions=[
		['content-length-range', 0, 41943040000]
	],
	ExpiresIn=86400
)

list_values = list(response.values())
url_value = list_values[0]
curl_cmd = url_value
all_values = dict(list_values[1])

for key,value in all_values.items():
	if key == "key":
		curl_cmd = "curl --request PUT --upload-file " + value + " " + curl_cmd
		curl_cmd += "/" + value
	if key == "AWSAccessKeyId":
		curl_cmd += "?" + value
	if key == "policy":
		curl_cmd += "%26" + value
	if key == "signature":
		curl_cmd += "%26" + value

curl_cmd += " -k"

print(curl_cmd)
