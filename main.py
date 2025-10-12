from src.agent.testing_agent import test_agent
import asyncio
from prompt.prompts import testcases_prompt
import json
from utils.load_feature_files import load_feature_files

with open("prerequsites/credentials.json", "r", encoding="utf-8") as f:
    credentials = json.load(f)


# from utils.get_user_story import get_user_story
# from utils.get_parent_folder import get_parent_folder
# high_level_story = get_user_story("prerequsites/parabank_user_story.md")
# parent_folder = get_parent_folder(high_level_story)
# testcases_prompt = testcases_prompt.format(
#     high_level_story=high_level_story,
#     credentials=credentials,
#     parent_folder=parent_folder
# )

task_id = "3"
testcases_prompt = testcases_prompt.format(
    task_id=task_id,
    credentials=credentials,
)

logs = []

if __name__ == "__main__":
    # Run the async main function
    rsp = input("Do you want to run the agent to generate test cases from the user story? (y/n): ")
    logs.append("Running agent to generate test cases from the user story")
    if rsp.lower() == 'y':
        response = asyncio.run(test_agent(testcases_prompt))
        for action, observation in response["intermediate_steps"]:
            logs.append(f"Thought: {action.log.split('Action:')[0].strip()}") # Extract thought from the log
            logs.append(f"Action: {action.tool}")
            logs.append(f"Action Input: {action.tool_input}")
            logs.append(f"Observation: {observation}")
            logs.append("-" * 20)
    logs.append("Finished running agent to generate test cases from the user story")
    logs.append("-"*40)
    logs.append("Running agent on the feature files created")
    rsp = input("Do you want to run the agent on the feature files created? (y/n): ")
    if rsp.lower() == 'y':
        folder_path = input("Enter the folder path where the feature files are located (e.g., features/): ").strip()
        features = load_feature_files(folder_path)
        for feature in features:
            from prompt.prompts import testing_prompt
            testing_prompt = testing_prompt.format(
                feature=feature
            )
            response = asyncio.run(test_agent(testing_prompt))
            for action, observation in response["intermediate_steps"]:
                logs.append(f"Thought: {action.log.split('Action:')[0].strip()}") # Extract thought from the log
                logs.append(f"Action: {action.tool}")
                logs.append(f"Action Input: {action.tool_input}")
                logs.append(f"Observation: {observation}")
                logs.append("-" * 20)
    logs.append("Finished running agent on the feature files created")
    # Save logs to a file
    with open("agent_thoughts.log", "w", encoding="utf-8") as f:
        f.write("\n".join(logs))
    
    # Run Critic Agent
    rsp = input("Do you want to run the Critic agent to evaluate the test cases created? (y/n): ")
    if rsp.lower() == 'y':
        from src.agent.critic_agent import main as run_critic_agent
        asyncio.run(run_critic_agent())