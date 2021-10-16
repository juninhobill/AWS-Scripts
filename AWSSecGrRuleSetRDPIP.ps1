#Powershell script to set automatically an IP Address in the Inbound Rules of a specific Security Group for an EC2 on AWS.
#Just set the Access Key, Secret Key and Region in the ps1 file and pass the following parameters when run the ps1 file:
#$currentIp = Your current IP Address.
#$obsoleteIp = Your old IP Address.
#$secGroupID = Your Security Group ID.
#$description = Your rule description, can be used to control the rule by user, for an example, you can check for some 
#user name (in the description field), if this user name exist and it is associated to an old IP Address, this script 
#will delete this old rule and create a new one, if it doesn't exist, the script will create a new rule with the IP 
#Address for the specific user name (in the description field). We are using that way in our organization and it is working like a charm.


Import-Module "C:\Program Files (x86)\AWS Tools\PowerShell\AWSPowerShell\AWSPowerShell.psd1"

$accessKey = ""
$secretKey = ""
$region = ""

$currentIp = $parameters["currentIp"]
$obsoleteIp = $parameters["obsoleteIp"]
$secGroupID = $parameters["secGroupID"]
$description = $parameters["description"]

function IsNullOrEmpty($str)
{
	If ($str)
	{
		return ($str -replace " ","" -replace "`t","").Length -eq 0
	}
	Else
	{
	return $true
	}
}

Try
{
If (IsNullOrEmpty($obsoleteIp))
	{
	$IpRange = New-Object -TypeName Amazon.EC2.Model.IpRange
	$IpRange.CidrIp = $currentIp + "/32"
	$IpRange.Description = $description
	$IpPermission = New-Object Amazon.EC2.Model.IpPermission
	$IpPermission.IpProtocol = "tcp"
	$IpPermission.FromPort = 3389
	$IpPermission.ToPort = 3389
	$IpPermission.Ipv4Ranges = $IpRange
	Grant-EC2SecurityGroupIngress -GroupId $secGroupId -IpPermission $IpPermission `
	-Region $region -AccessKey $accessKey -SecretKey $secretKey
	}
	Else
	{
	$ipInSecurityGroup = @{IpProtocol="tcp"; FromPort="3389"; ToPort="3389"; IpRanges=$obsoleteIp}
	Revoke-EC2SecurityGroupIngress -GroupId $secGroupId -IpPermissions $ipInSecurityGroup `
	-Region $region -AccessKey $accessKey -SecretKey $secretKey	
	
	$IpRange = New-Object -TypeName Amazon.EC2.Model.IpRange
	$IpRange.CidrIp = $currentIp + "/32"
	$IpRange.Description = $description
	$IpPermission = New-Object Amazon.EC2.Model.IpPermission
	$IpPermission.IpProtocol = "tcp"
	$IpPermission.FromPort = 3389
	$IpPermission.ToPort = 3389
	$IpPermission.Ipv4Ranges = $IpRange
	Grant-EC2SecurityGroupIngress -GroupId $secGroupId -IpPermission $IpPermission `
	-Region $region -AccessKey $accessKey -SecretKey $secretKey
	}
}
Catch
{
$ErrorMessage = $_.Exception.Message
$ErrorMessage
Break
}
