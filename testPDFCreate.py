from fpdf import FPDF
import requests
from langchain_openai import AzureChatOpenAI
from langchain.adapters.openai import convert_openai_messages
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

MODEL = os.getenv('MODEL', 'gpt-4-turbo')
api_key = os.getenv('API_KEY')
azure_endpoint = os.getenv('AZURE_ENDPOINT')
api_version_llm = os.getenv('API_VERSION_LLM', '2024-08-01-preview')
api_version_embedding = os.getenv('API_VERSION_EMBEDDING', '2023-05-15')

text = """Business Requirement Document (BRD)
1. Project Objectives:
- Develop a scalable new platform that handles the current user load and anticipates future growth,
potentially reaching 10 million active users by Q2 next year.
- Incorporate advanced features such as messaging encryption and group video calls to enhance user
experience.
- Ensure seamless integration with existing marketing and analytics tools, maintaining robust data
collection and user targeting capabilities.
2. Stakeholders:
- John (Product Manager): Leading the project and coordinating between teams.
- Sarah (Lead Developer): Key in researching and proposing technical solutions.
- Emily (Marketing Manager): Responsible for aligning platform capabilities with marketing strategies.
- David (Data Analyst): Provides insights on user data to inform platform scaling.
3. Functional Requirements:
- The platform must support an increased user load up to 10 million active users efficiently.
- Must include new features like advanced messaging encryption and group video calls.
- Needs to have robust API access for integration with existing tools.
- Data migration strategies must be implemented to transition from the old platform without user
disruption.
4. Non-Functional Requirements:
- Scalability: The platform should efficiently scale to accommodate growth.
- Performance: Optimized to handle high user volumes with minimal latency.
- Security: Enhanced security measures, particularly for new features like encryption.
- Reliability: Stable operation during peak loads, especially in holiday seasons.
5. Constraints:
- The migration process must minimize disruption for current users, potentially requiring a phased rollout.
- The development timeline must consider the holiday season, avoiding major updates during peak user
activity.
- Decision-making between in-house versus cloud-based solutions needs balancing factors such as cost,
control, scalability, and time-to-market.
This document captures the comprehensive requirements and considerations discussed during the new
product platform meeting. The project aims to revamp the existing platform to support rapid user growth
and integrate advanced features, ensuring a seamless transition and enhanced user experience."""

prompt = [{
            "role": "system",
            "content": "you are a helpful assistant that writes some code."
        }, {
            "role": "user",
            "content":     f""""You are given some text below.
                            You will use FPDF python package and the code should be in python. Do not give the import packages and do not write a function. Just give the code block and nothing else. No explanation is needed"""
                       f"Please return nothing but the code block. The text should be formatted properly, with headings, proper indentation and bullets. The font sizes should be such that the heading size should be larger and bold and the bullet headers should be smaller.The lines should fit within the page and should not exceed the page.\n"
                       f"{text}\n "
        }]

lc_messages = convert_openai_messages(prompt)

response = AzureChatOpenAI(model="gpt-4",azure_deployment="gpt-4",api_key=api_key,azure_endpoint=azure_endpoint,api_version=api_version_llm).invoke(lc_messages).content

# Data you want to send in the POST request

print(response)

exec(response)
