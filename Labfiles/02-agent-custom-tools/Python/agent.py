import os
import json
from dotenv import load_dotenv

# Add references

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FunctionTool
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import PromptAgentDefinition, FunctionTool
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam
from functions import next_visible_event, calculate_observation_cost, generate_observation_report


def main(): 
    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    # Load environment variables from .env file
    load_dotenv()
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

    # Connect to the project client
    with(
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
        project_client.get_openai_client() as openai_client
    ):
    

        # Define the event function tool
        event_tool = FunctionTool(
            name="get_next_visible_event",
            description="Get the next visible astronomy event for a given location and date.",
            parameters={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description":"continent to find the next visible event in (e.g. 'north_america', 'south_america', 'australia')"
                    },
                },
                "required": ["location"],
                "additionalProperties": False,
            },
            strict=True
        )
        

        # Define the observation cost function tool
        observation_cost_tool = FunctionTool(
            name="calculate_observation_cost",
            description= "Calculate the cost of an observation based on the type of event and the equipment used.",
            parameters={
                "type": "object",
                "properties": {
                    "telescope_tier": {
                        "type": "string",
                        "description": "The tier of the telescope used for the observation (e.g. 'standard', 'advanced', 'premium')"
                        },
                        "hours":{
                            "type": "number",
                            "description": "The number of hours the telescope will be used for the observation"
                        },
                        "priority":{
                            "type": "string",
                            "description": "The priority level of the observation (e.g. 'low', 'medium', 'high')"
                        },
                },
                        "required": ["telescope_tier", "hours", "priority"],
                        "additionalProperties": False,

                
            },
            strict=True
        )
        

        # Define the observation report generation function tool
        report_tool = FunctionTool(
            name="generate_observation_report",
            description= "Generate a report summarizing the details of an astronomy observation.",
            parameters={
                "type": "object",
                "properties": {
                    "event_name": {
                        "type": "string",
                        "description": "The name of the astronomy event being observed"
                    },
                    "observation_date": {
                        "type": "string",
                        "description": "The date of the observation in YYYY-MM-DD format"
                    },
                    "location": {
                        "type": "string",
                        "description": "The location of the observation"
                    },
                    "telescope_used": {
                        "type": "string",
                        "description": "The type of telescope used for the observation"
                    },
                    "observation_cost": {
                        "type": "number",
                        "description": "The cost of the observation in USD"
                    }
                },
                "required": ["event_name", "observation_date", "location", "telescope_used", "observation_cost"],
                "additionalProperties": False,
            },
            strict=True
        )
        

        # Create a new agent with the function tools
        agent = project_client.agents.create_version(
            agent_name="astronomy-agent",
            definition=PromptAgentDefinition(
                model=model_deployment,
                tools=[event_tool, observation_cost_tool, report_tool],
                instructions="You are an astronomy assistant that helps users find information about astronomy events, calculate observation costs, and generate observation reports."         
        )
        )
        
        
        # Create a thread for the chat session
        conversation = openai_client.conversations.create()
        
        
        
        while True:
            user_input = input("Enter a prompt for the astronomy agent. Use 'quit' to exit.\nUSER: ").strip()
            if user_input.lower() == "quit":
                print("Exiting chat.")
                break

            # Send a prompt to the agent
            openai_client.conversations.items.create(
                conversation_id=conversation.id,
                items=[{"type": "message", "role": "user", "content": user_input}],
            )

           
        
            # Retrieve the agent's response, which may include function calls
            response= openai_client.responses.create(
                conversation=conversation.id,
                extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}}
            )
            if response.status == "failed":
                print(f"Response failed: {response.error}")

            input_list = []
            # Process function calls
            for item in response.output:
                if item.type == "function_call":
                    function_name = item.name
                    result = None
                    if item.name == "get_next_visible_event":
                        result = next_visible_event(**json.loads(item.arguments))
                    elif item.name == "calculate_observation_cost":
                        result = calculate_observation_cost(**json.loads(item.arguments))
                    elif item.name == "generate_observation_report":
                        result = generate_observation_report(**json.loads(item.arguments))

                    input_list.append(
                        FunctionCallOutput(
                            type="function_call_output",
                            call_id=item.call_id,
                            output=result
                        )
                    )        



            

            # Send function call outputs back to the model and retrieve a response
            if input_list:
                response= openai_client.responses.create(
                    input=input_list,
                    previous_response_id=response.id,
                    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
                )
            print(f"AGENT: {response.output_text}")    
            

        # Delete the agent when done
        project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
        print("Deleted agent.")
        

if __name__ == '__main__': 
    main()