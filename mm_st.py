import os
import streamlit as st
import mm_agent
from tinydb import TinyDB
import requests
import json
from fpdf import FPDF
import base64
from langchain.adapters.openai import convert_openai_messages
from langchain_openai import  AzureChatOpenAI,ChatOpenAI
from langgraph.graph import Graph
from mytools import load_text_from_path,extract_text

DB_FILE = 'db.json'
flow = 509



if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

def process_form(form_number,article):
    def set_value():
        print("set value",st.session_state.url)
        st.session_state["newvalues"]["url"]=st.session_state.url
        del st.session_state.newvalues["next"]
        
    def set_file():
        st.session_state["newvalues"].update({"raw":st.session_state.input_file.getvalue(),
                                     "file_name":st.session_state.input_file.name})
        del st.session_state.newvalues["next"]

    def do_first_dialog():
        words_in_article = st.slider("Words in Document", 100, 20000, 500)

        # Radio buttons
        source_document = st.radio("Retrieve source document from:", ["cloud", "my computer", "existing BRD Document"])
        
        # Buttons and logic
        if st.button('OK'):
            val = "upload"
            if source_document== "cloud":
                val = "internet"
            elif source_document== "existing BRD Document":
                val = "BRD"
            else:
                val = "upload"
            st.session_state['newvalues']={'origin': val,
                                           "words":words_in_article,"next":True}
            st.rerun()
        
        # Assuming you want to use the dictionary elsewhere after pressing OK
       
        
    #print(form_number,article)
    if form_number==0:
        if "origin" in article: #if initial dialog happened
            st.session_state["newvalues"]["direct_story"]=False
            if article["origin"]=="internet":
                st.text_input("Enter the URL of your source document:",key="url",
                                                           on_change=set_value)
            else: #if have to upload file
                st.file_uploader('Choose your source document',
                                      type=['pdf','docx','html','txt'],
                                      accept_multiple_files=False,
                                      help="""
                                      This is the source for the BRD you want to generate.
                                      It contains the transcripts of your meeting.
                                      It can be a pdf, docx, html, or text file
                                      """,
                                      on_change=(set_file),
                                      key="input_file"
                                      )
                if article["origin"]=="BRD":
                    st.session_state["newvalues"]["direct_story"]=True
                    
        if not "origin" in article: #if this is initial dialog
            do_first_dialog()

    elif form_number==1:
        # header = article["title"]
        # st.title(header)
                
        # Instructions (if any)
        instruction_text = "Here is your Business Requirement Document. \nYou can edit either the BRD document or the critique.\n Clear the critique to use the BRD as displayed. "
        if instruction_text:
            st.write(instruction_text)
        
        # Text Boxes and Labels
        initial_contents = [article["body"],article["critique"]]  
        titles = ["Draft BRD", "Critique"] 
        
        text_boxes = []
        for content, title in zip(initial_contents, titles):
            st.subheader(title)
            text_input = st.text_area("", value=content, height=300 if titles.index(title) == 0 else 150)
            text_boxes.append(text_input)
        
        if "url" in article:
            link_text = "Click here to open source document in browser."
            link_url = article["url"]
            st.markdown(f"[{link_text}]({link_url})", unsafe_allow_html=True)

        # OK Button
        if st.button('OK'):
            # Perform actions based on the form submission here
            # For example, print or store the contents of text_boxes

            st.session_state["newvalues"]={"body":text_boxes[0],"critique":text_boxes[1],"button":"OK"}

def generate_pdf(text):
    MODEL='gpt-4'
    api_key = "AjIyl8hhQxEq4v4an3Cq3wfk68xYKY5O7RWeuvdwLJXKE9UXZlomJQQJ99BCACYeBjFXJ3w3AAAAACOGrCpt"
    azure_endpoint = "https://march25.cognitiveservices.azure.com/"
    api_version_llm = "2024-08-01-preview"
    api_version_embedding = "2023-05-15"

    prompt = [{
                "role": "system",
                "content": "you are a helpful assistant that writes some code."
            }, {
                "role": "user",
                "content":     f""""You are given some text below.
                                You will use FPDF python package and the code should be in python. Do not give the import packages and do not write a function. Just give the code block and nothing else. No explanation is needed"""
                        f"Add a subheader: 'Authored By: Sarbo Mitra' in the pdf"        
                        f"Please return nothing but the code block. The text should be formatted properly, with headings, proper indentation and bullets. The font sizes should be such that the heading size should be larger and bold and the bullet headers should be smaller.The lines should fit within the page and should not exceed the page.\n"
                        f"The file name should be 'BRD_formatted.pdf'"
                        f"Do not write anything else. Just give the code. Do not write ```python at first. Just the code and nothing else."
                        f"Text:\n"
                        f"{text}\n "
            }]

    lc_messages = convert_openai_messages(prompt)

    response = AzureChatOpenAI(model="gpt-4",azure_deployment="gpt-4",api_key=api_key,azure_endpoint=azure_endpoint,api_version=api_version_llm).invoke(lc_messages).content

    # Data you want to send in the POST request
    exec(response)


def rerun():
    st.session_state['dm'] = None
    st.session_state['result']=None
    st.session_state["newvalues"]=None
    #st.session_state["direct_story"]=False
           
# Initialize session state
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = None
    st.session_state['dm'] = None
    st.session_state['result']=None
    st.session_state["newvalues"]=None
    st.session_state["BRD_over"]=None
    #st.session_state["direct_story"]=False

def UserStoryText(json):
    api_key = "AjIyl8hhQxEq4v4an3Cq3wfk68xYKY5O7RWeuvdwLJXKE9UXZlomJQQJ99BCACYeBjFXJ3w3AAAAACOGrCpt"
    azure_endpoint = "https://march25.cognitiveservices.azure.com/"
    api_version_llm = "2024-08-01-preview"
    api_version_embedding = "2023-05-15"
    sample_json = """
            [
                {
                    "title": title of the user story,
                    "description": description of the user story,
                    "acceptance_criteria": acceptance criteria of the user story,
                    "story_points": story points of the user story
                }
            ]
         
               """
    prompt = [{
        "role": "system",
        "content": "You are a json-to-text convertor that transforms the json into a proper markdown."
    }, {
        "role": "user",
        "content": f""""You have a json that describes user stories, which contains fields title, description, user story point and acceptance criteria. """
                    f"The json should be converted into a proper markdown document that is properly formatted. Do not give any title, explanation or anything extra.Do not give anything other than the contents of the markdown."
                    f"JSON:\n"
                    f"{json}\n"
    }]

    lc_messages = convert_openai_messages(prompt)
    response = AzureChatOpenAI(model="gpt-4",azure_deployment="gpt-4",api_key=api_key,azure_endpoint=azure_endpoint,api_version=api_version_llm).invoke(lc_messages).content
    return response

def UserStoryJson(text):
    api_key = "AjIyl8hhQxEq4v4an3Cq3wfk68xYKY5O7RWeuvdwLJXKE9UXZlomJQQJ99BCACYeBjFXJ3w3AAAAACOGrCpt"
    azure_endpoint = "https://march25.cognitiveservices.azure.com/"
    api_version_llm = "2024-08-01-preview"
    api_version_embedding = "2023-05-15"
    sample_json = """
            [
                {
                    "title": title of the user story,
                    "description": description of the user story,
                    "acceptance_criteria": acceptance criteria of the user story,
                    "story_points": story points of the user story
                }
            ]
         
               """
    prompt = [{
        "role": "system",
        "content": "You are a text-to-json convertor that transforms a markdown text to a json."
    }, {
        "role": "user",
        "content":  f""""You have a formatted text that contains information regarding some user stories. Convert the text to a json that describes user stories, which contains fields title, description, user story point and acceptance criteria."""
                    f"The text should be converted into a json array an example of which is given below. Do not give any title, explanation or anything extra.Do not give anything other than the contents of the markdown."
                    f"JSON:\n"
                    f"{json}\n"
                    f"Text:\n"
                    f"{text}"
    }]

    lc_messages = convert_openai_messages(prompt)
    response = AzureChatOpenAI(model="gpt-4",azure_deployment="gpt-4",api_key=api_key,azure_endpoint=azure_endpoint,api_version=api_version_llm).invoke(lc_messages).content
    return response

def UserStory(the_text):
    api_key = "AjIyl8hhQxEq4v4an3Cq3wfk68xYKY5O7RWeuvdwLJXKE9UXZlomJQQJ99BCACYeBjFXJ3w3AAAAACOGrCpt"
    azure_endpoint = "https://march25.cognitiveservices.azure.com/"
    api_version_llm = "2024-08-01-preview"
    api_version_embedding = "2023-05-15"
    sample_json = """
            [
                {
                    "title": title of the user story,
                    "description": description of the user story,
                    "acceptance_criteria": acceptance criteria of the user story,
                    "story_points": story points of the user story
                }
            ]
         
               """
    prompt = [{
        "role": "system",
        "content": "You are a scrum master who creates User Stories from Business Requirement Documents"
    }, {
        "role": "user",
        "content": f""""You have deep knowledge of user stories those are created in Azure Devops.
                        Generate user stories, you should provide title,description, user story point and acceptance criteria from the BRD(Business Requirement Document) that is provided below"""
                    f"The output should be in json format. Do not give any title, explanation or anything extra.Do not give anything other than a JSON"
                    f"The sample json for one user story is attached. Simply add the user stories in the json array."
                    f"Sample JSON:\n"
                    f"{sample_json}\n"
                    f"BRD:\n"
                    f"{the_text}\n"

    }]
    lc_messages = convert_openai_messages(prompt)
    response = AzureChatOpenAI(model="gpt-4",azure_deployment="gpt-4",api_key=api_key,azure_endpoint=azure_endpoint,api_version=api_version_llm).invoke(lc_messages).content
    st.session_state["result"] = response
    st.session_state["BRD_over"] = 1

def ado_deploy(i,Stories):
    stories = json.loads(Stories)
    
    # stories = Stories
    url = "https://dev.azure.com/pwc-gx-gi/DevOps%20Space/_apis/wit/workitems/$User%20Story?api-version=7.1"
    key = "3g30uHOcLR2jjC5HFOBNytJahPPOQuXo3RDt9mJB2EIzQ76EIAASJQQJ99BCACAAAAACqLzhAAASAZDO2ZHY"
    for item in stories:
        i = i + 1
        title = item["title"]
        description = item["description"]
        acceptance = item["acceptance_criteria"]
        storypoint = item["story_points"]
        
        payload = [
        {
            "op": "add",
            "path": "/fields/System.Title",
            "from": None,
            "value": f"{title}"
        },
        {
            "op": "add",
            "path": "/fields/System.Description",
            "from": None,
            "value": f"{description}"
        },
        {
            "op": "add",
            "path": "/fields/Microsoft.VSTS.Scheduling.StoryPoints",
            "from": None,
            "value": f"{storypoint}"
        },
        {
            "op": "add",
            "path": "/fields/Microsoft.VSTS.Common.AcceptanceCriteria",
            "from": None,
            "value": f"{acceptance}"
        }
        ]
        # print(payload)
        print("\n")
        headers = {
            'Content-Type': "application/json-patch+json",
            'Authorization': "Bearer 3g30uHOcLR2jjC5HFOBNytJahPPOQuXo3RDt9mJB2EIzQ76EIAASJQQJ99BCACAAAAACqLzhAAASAZDO2ZHY"
        }
        response = requests.post(url, json=payload,headers=headers)
        # print(response.json())
        if response.status_code == 200:
            st.markdown("User Story "+str(i)+" added")
           
def on_button_click():
    st.session_state.button_clicked = True



# App title
st.title("Service Request Agent")
st.html("<h2>Business Requirement Document and Product Features Generation</h2>")

# if(st.session_state["direct_story"]==True):
#     fileName = st.session_state.newvalues["file_name"]
#     if "raw" in st.session_state["newvalues"]: #if already read
#         the_text=extract_text(content=st.session_state["newvalues"]['raw'],content_type=st.session_state["newvalues"]["file_name"].split('.')[-1])
#         del st.session_state["newvalues"]["raw"]
#     else:
#         the_text=load_text_from_path(st.session_state["newvalues"]['file_name'])
#     UserStory(the_text)

# Sidebar for API key input

if not st.session_state.api_key:
    #with st.sidebar:
    api_key=st.text_input("Enter your password to get started:",type='password')
    # st.markdown("You can also use the custom GPT version free without an API key or a paid subscription by clicking [here](https://chatgpt.com/g/g-roNR24Ty6-collaborative-meeting-reporter).",
    #             unsafe_allow_html=True)
    if api_key:
        st.session_state['api_key'] =api_key
        st.rerun()
 

if st.session_state['api_key'] and st.session_state["dm"] is None:
    os.environ['OPENAI_API_KEY'] = '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'
    st.session_state['dm'] = mm_agent.StateMachine()
    st.session_state["result"] = st.session_state['dm'].start()
  
if st.session_state["result"]:
    print("have result")
    #st.session_state['BRD_Over'] = 0
    #st.session_state["newvalues"]
    if "quit" not in st.session_state['result']:
        if st.session_state["BRD_over"]:
            Stories = st.session_state['result']
            #stories = json.loads(Stories)
            story_formatted = UserStoryText(Stories)
            st.markdown("The following User Stories have been generated:-")
            # user_story = ""
            # i = 0
            # for item in stories:
            #     i = i + 1
            #     #user_story = user_story + str(i)+")"+item["title"]+"\n"+"Description:\n"+item["description"]+"\nAcceptance Criteria:\n"+item["acceptance criteria"]+"\nStory Point:\n"+item["Story Points"]+"\n"
            #     st.html("<h3>"+str(i)+")"+item["title"]+"</h3>")
            #     st.html("<h4>Description:</h4>")
            #     st.markdown(item["description"])
            #     st.html("<h4>Acceptance Criteria:</h4>")
            #     st.markdown(item["acceptance criteria"])
            #     st.html("<h4>Story Point:</h4>")
            #     st.markdown(item["Story Points"])

            text_input = st.text_area("", value=story_formatted, height=300)

            if st.button('OK'):
            # Perform actions based on the form submission here
            # For example, print or store the contents of text_boxes
                
                story_json = UserStoryJson(text_input)

                print(story_json)  

                st.session_state["result"] = story_json
        
            #st.markdown(st.session_state["result"])

            #st.download_button(label='User Story File',data=st.session_state["result"],file_name="User.csv",type="primary",mime="text/csv")
            with st.sidebar:
                st.button("Run with new document",key="rerun1",on_click=rerun)
                with st.spinner("Please wait. Your User Stories are being added to ADO Board...."):
                    #st.button("Generate",key="User Story Generation",on_click=ado_deploy(st.session_state["result"]))
                    st.button('Generate', on_click=on_button_click)
                    if st.session_state.button_clicked:
                       ado_deploy(0,st.session_state["result"])
                       #ado_deploy(0,st.session_state["result"])
            
        else:
            if st.session_state["newvalues"] is None:
                process_form(st.session_state['result']["form"],st.session_state['result'])                
            if st.session_state["newvalues"] and "next" in st.session_state.newvalues:
                process_form(st.session_state['result']["form"],st.session_state.newvalues)

            if st.session_state["newvalues"] and not "next" in st.session_state.newvalues:
               
                #if len(st.session_state["newvalues"]["url"])>0:
                    print("*********")
                    #st.session_state["newvalues"]
                    with st.spinner("Please wait. Your BRD is being generated...."):
                        st.session_state["result"]=st.session_state['dm'].resume(st.session_state["newvalues"])
                    st.session_state["newvalues"]=None
                    st.rerun()


    if "quit" in st.session_state["result"]:
        st.subheader(st.session_state.result["title"])
        st.write(st.session_state.result["date"])
        st.markdown(st.session_state.result["body"])
        st.write("\n")
        st.write("summary:",st.session_state.result["summary"])
        
        if st.button('Submit for Review',type='primary'):
            # URL you want to send the POST request to
            url = "https://prod-92.westeurope.logic.azure.com:443/workflows/858bd1dfc82a4b6a9816cb27f1259bdc/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=aRAzQalF1t27Nfx6sLW1CY4u7URrkf5YD27e2WhYk3Y"

            # Data you want to send in the POST request
            data = {
                'body': st.session_state.result["body"],
                'user': st.session_state['api_key']
            }
            headers = {'Content-Type': "application/json"}
            # Sending the POST request with SSL verification turned off
            with st.spinner("Please wait. We have sent your BRD for approval to the Approver...."):
                response = requests.post(url, json=data,verify=False)
            status = response.text
            flow = response.status_code
            #The final status
            st.markdown(status)
            with st.spinner("Please wait. Your BRD is being created...."):
                generate_pdf(st.session_state.result["body"])
            with open("BRD_formatted.pdf", "rb") as f:
                st.download_button(label='Download BRD Document',data=f,file_name="BRD_doc.pdf",type="primary")
                
        
        with st.sidebar:
            st.button("Run with new document",key="rerun1",on_click=rerun)
            st.button("Generate User Stories",type='primary',on_click=UserStory(st.session_state.result["body"]))

           
            
                



        
            


    


