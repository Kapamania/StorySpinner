import requests
import json

Stories = """[ { "title": "Support for 10 Million Active Users", "description": "Develop a platform that supports a minimum of 10 million active users with capabilities for further scalability.", "acceptance criteria": "Platform must demonstrate it can handle up to 10 million active users concurrently without performance degradation.", "Story Points": 8 }, { "title": "Integrate Advanced Messaging and Video Call Features", "description": "Incorporate advanced features such as messaging encryption and group video calls into the platform.", "acceptance criteria": "Messaging encryption and group video calls should function seamlessly and meet security standards.", "Story Points": 5 }, { "title": "Integration with Marketing and Analytics Tools", "description": "Ensure the new platform integrates seamlessly with existing marketing and analytics tools.", "acceptance criteria": "Successful data exchange and functionality between the new platform and existing marketing and analytics tools without data loss.", "Story Points": 3 }, { "title": "Provide Robust API Access", "description": "Develop robust API access to facilitate easy integration with external systems and services.", "acceptance criteria": "APIs should provide full functionality as required by external systems, with comprehensive documentation and no critical bugs.", "Story Points": 5 }, { "title": "Implement Phased Migration Strategy", "description": "Create a phased migration strategy to transition from the old to the new platform with minimal user disruption.", "acceptance criteria": "Users experience no significant downtime or loss of data during migration, and report satisfactory performance of the new platform.", "Story Points": 5 }, { "title": "Platform Performance Optimization", "description": "Optimize the platform to manage increased traffic and user load with minimal latency.", "acceptance criteria": "Platform maintains a response time of less than 2 seconds under peak load conditions.", "Story Points": 3 }, { "title": "Implement Enhanced Security Measures", "description": "Enhance security measures, including advanced encryption for messaging services, to protect user data.", "acceptance criteria": "All messaging data should be encrypted with up-to-date encryption standards and pass security audits without critical issues.", "Story Points": 5 }, { "title": "Ensure Platform Scalability", "description": "Design the platform architecture to allow for easy scalability to accommodate future growth.", "acceptance criteria": "The platform should be able to scale up to handle 20 million users without major architectural changes.", "Story Points": 5 }, { "title": "Maintain High Platform Reliability", "description": "Achieve high uptime and minimal service disruptions for the platform.", "acceptance criteria": "Platform should have an uptime of 99.9% and all service disruptions should be resolved within 1 hour.", "Story Points": 5 }, { "title": "Preserve Data Integrity During Migration", "description": "Ensure the integrity and continuity of existing user data is preserved during the migration phase.", "acceptance criteria": "No loss or corruption of user data during migration, with a successful data validation post-migration.", "Story Points": 5 } ]"""


stories = json.loads(Stories)
    # stories = Stories
url = "https://dev.azure.com/pwc-gx-gi/DevOps%20Space/_apis/wit/workitems/$User%20Story?api-version=7.1"
key = "3g30uHOcLR2jjC5HFOBNytJahPPOQuXo3RDt9mJB2EIzQ76EIAASJQQJ99BCACAAAAACqLzhAAASAZDO2ZHY"
for item in stories:
    title = item["title"]
    description = item["description"]
    acceptance = item["acceptance criteria"]
    storypoint = item["Story Points"]
    
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
        # Parse the JSON response
        data = response.json()
        print(data)