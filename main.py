import os
import dotenv
import boto3
from pprint import pprint
dotenv.load_dotenv()
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_react_agent, AgentExecutor
# from langgraph.prebuilt import create_react_agent
from langchain.tools import Tool

aws_mngmnt = boto3.session.Session(profile_name="default")

def listec2instance():
    """
    This function returns the name and id of all running EC2 instances.
    """
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
    pprint(instances)
    return instances

def createec2instance():
    """
    This function creates an EC2 instance.
    """
    ec2 = aws_mngmnt.client("ec2")
    res = ec2.run_instances(
        ImageId='ami-0e35ddab05955cf57',
        InstanceType='t2.micro',
        MaxCount=1,
        MinCount=1,
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [{"Key": "Name", "Value": "createdfromboto3"}]
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

    _template = """
    You know Hindi and English language.
    You have tools to perform actions on AWS account.
    Based on the user's query you need to perform those actions using the one or more tools.
    Perform the requested action using the tool only and return results in a structured format.
    Use JSON format for structured data.

    Question: {query}
    """

    prompt_template = PromptTemplate(
        input_variables = ["query"], 
        template = _template
    )

    tools_for_agent = [
        Tool(name="List EC2 Instances", func=listec2instance, description="Gets all running EC2 instances"),
        Tool(name="Create EC2 Instance", func=createec2instance, description="Creates an EC2 instance."),
        Tool(name="Stop EC2 Instance", func=stopec2instance, description="Stops an EC2 instance given an ID."),
    ]

    llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-2.0-flash", verbose=True)

    _query = "List all the active EC2 instances."
    
    # chain = prompt_template | llm 
    # result = chain.invoke(input={"query":_query})

    agent = create_react_agent(tools=tools_for_agent, llm=llm)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke({"input": _query})
    pprint(result)
