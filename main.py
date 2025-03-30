import os
import dotenv
import json
import boto3
from pprint import pprint
dotenv.load_dotenv()
from langchain import hub
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_react_agent, AgentExecutor
# from langgraph.prebuilt import create_react_agent
from langchain.tools import Tool

aws_mngmnt = boto3.session.Session(profile_name="default")

def listec2instance(*args):
    """
    This function returns the name and id of all running EC2 instances.
    """
    # print("Called List EC2 instances, with these args-", args)
    ec2 = aws_mngmnt.client("ec2")
    response = ec2.describe_instances(
        Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
    )

    instances = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            name = next(
                (tag["Value"] for tag in instance.get("Tags", []) if tag["Key"] == "Name"),
                "Unnamed Instance",
            )
            instances.append({"Instance ID": instance_id, "Name": name})
    # pprint(instances)
    return instances

def createec2instance(name: str):
    """
    This function creates an EC2 instance.
    """
    name = name.split(':')[-1].strip()
    # print("Name to be created with- ",name)
    ec2 = aws_mngmnt.client("ec2")
    res = ec2.run_instances(
        ImageId='ami-0e35ddab05955cf57',
        InstanceType='t2.micro',
        MaxCount=1,
        MinCount=1,
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [{"Key": "Name", "Value": name}]
            }
        ]
    )
    return {"Message": "Instance created", "Instance ID": res["Instances"][0]["InstanceId"]}

def stopec2instance(instance_id):
    """
    This function stops an EC2 instance.
    """
    ec2 = aws_mngmnt.client("ec2")
    response = ec2.stop_instances(InstanceIds=[instance_id])
    return {"Message": "Instance stopped", "Instance ID": instance_id}

if __name__ == "__main__":
    print("Let's get this started")

    tools_for_agent = [
        Tool(name="List EC2 Instances", func=listec2instance, description="Gets all running EC2 instances"),
        Tool(name="Create EC2 Instance", func=createec2instance, description="Creates an EC2 instance."),
        Tool(name="Stop EC2 Instance", func=stopec2instance, description="Stops an EC2 instance given an ID."),
    ]

    llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-2.0-flash")

    # _query = "List all the active EC2 instances."
    _query = "Mere jitne EC2 instances hai woh batao."
    # _query = "Make an EC2 instance with the name shasankperiwal."
    # _query = "Ek EC2 instance banana shasankperiwal2 naam se."
    # _query = "woh shasankperiwal naam wala ec2 instance delete kar dena pls"
    
    prompt_template = hub.pull("hwchase17/react")
    agent = create_react_agent(tools=tools_for_agent, llm=llm, prompt=prompt_template)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent)

    result = agent_executor.invoke({"input": _query})
    pprint(result["output"])
