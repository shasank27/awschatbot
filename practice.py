import boto3

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