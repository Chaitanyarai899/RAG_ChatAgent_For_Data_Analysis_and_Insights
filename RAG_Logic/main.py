
from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI
import pandas as pd
import chainlit as cl
import io

import sys
import os
sys.path.append(os.path.abspath('.'))

from chainlit import user_session

user_env = user_session.get("env")

# Chainlit fetches env variables from .env automatically

""" from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
"""


def create_agent(data: str, llm):
    """Create a Pandas DataFrame agent."""
    return create_pandas_dataframe_agent(llm, data, verbose=False)


@cl.on_chat_start
async def on_chat_start():

    files = None

    # Waits for user to upload csv data
    while files == None:
        files = await cl.AskFileMessage(
            content="Please upload a csv file to begin!", accept=["text/csv"], max_size_mb= 100
        ).send()

    # load the csv data and store in user_session
    file = files[0]
    csv_file = io.BytesIO(file.content)
    df = pd.read_csv(csv_file, encoding="utf-8")

    # creating user session to store data
    cl.user_session.set('data', df)

    # Send response back to user
    await cl.Message(
        content=f"`{file.name}` uploaded! Now you ask me anything related to your data"
    ).send()


@cl.on_message
async def main(message: str):

    # Get data
    df = cl.user_session.get('data')

    user_env = cl.user_session.get("env")
    os.environ["OPENAI_API_KEY"] = user_env.get("OPENAI_API_KEY")

    # llm
    llm = OpenAI()

    # Agent creation
    agent = create_agent(df, llm)

    # Run model 
    response = agent.run(message)

    # Send a response back to the user
    await cl.Message(
        content=response,
    ).send()
