import boto3
from pprint import pprint

aws_mngmnt = boto3.session.Session(profile_name="default")
iam_cnsl = aws_mngmnt.resource("iam")
ec2_cnsl = aws_mngmnt.client("ec2")

dir(aws_mngmnt)
for user in iam_cnsl.users.all():
    print(user.name)

# for instance in ec2_cnsl.instances.all():
#     print(instance.id)
print(ec2_cnsl.describe_instances()["Reservations"][0]["Instances"][0]["Tags"][0]["Value"])
# print(ec2_cnsl.list_instances())
# SourceDestCheck)
# for instance in ec2_cnsl.describe_instances():
#     print(instance)

ec2 = boto3.client("ec2")

# Get running instances with their Name tags
response = ec2.describe_instances(
    Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
)

# Extract instance names
instances = []
for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        instance_id = instance["InstanceId"]

        name = next(
            (tag["Value"] for tag in instance.get("Tags", []) if tag["Key"] == "Name"),
            "Unnamed Instance",
        )
        instances.append({"Instance ID": instance_id, "Name": name})

print(instances)

# Create ec2 instance
# res = ec2.run_instances(
#     ImageId = 'ami-0e35ddab05955cf57',
#     InstanceType = 't2.micro',
#     MaxCount = 1,
#     MinCount = 1,
#     TagSpecifications=[
#         {
#             "ResourceType": "instance",
#             "Tags": [
#                 {"Key": "Name", "Value": "createdfromboto3"}
#             ]
#         }
#     ]
# )
# print("Bucket created- ", res)

s3_client = aws_mngmnt.client("s3")

# s3_list_res = s3_client.list_objects(Bucket = 'shasank-bucket')
# pprint(s3_list_res)

s3_get_res = s3_client.get_object(Bucket = 'shasank-bucket', Key= 'to_download/download.jpeg')
pprint(s3_get_res['Body'])

content = s3_get_res['Body'].read()
# pprint(content)
# with open("downloadedfroms3.jpg", "wb") as f:
#     f.write(content)