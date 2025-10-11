from src.agent.testing_agent import test_agent
import asyncio
from prompt.prompts import testing_prompt, testcases_prompt
import json
from utils.get_user_story import get_user_story
from utils.get_parent_folder import get_parent_folder
from utils.load_feature_files import load_feature_files

features = load_feature_files("autogen")

with open("prerequsites/credentials.json", "r", encoding="utf-8") as f:
    credentials = json.load(f)

high_level_story = get_user_story("prerequsites/parabank_user_story.md")
parent_folder = get_parent_folder(high_level_story)

testcases_prompt = testcases_prompt.format(
    high_level_story=high_level_story,
    credentials=credentials,
    parent_folder=parent_folder
)

if __name__ == "__main__":
    # Run the async main function
    rsp = input("Do you want to run the agent to generate test cases from the user story? (y/n): ")
    if rsp.lower() == 'y':
        asyncio.run(test_agent(testcases_prompt))
    rsp = input("Do you want to run the agent on the feature files created? (y/n): ")
    if rsp.lower() == 'y':
        for feature in features:
            testing_prompt = testing_prompt.format(
                feature=feature,
                high_level_story=high_level_story,
                credentials=credentials,
                parent_folder=parent_folder
            )
            asyncio.run(test_agent(testing_prompt))