# StorySpinner

StorySpinner is an innovative tool designed to transform meeting transcripts and call recordings into comprehensive Business Requirement Documents (BRDs) and user stories. This tool streamlines the documentation process, ensuring that all critical details from meetings are captured and converted into actionable insights.

## Problem Definition

In many organizations, the process of converting meeting discussions into actionable documents is time-consuming and prone to errors. StorySpinner addresses this problem by automating the generation of BRDs, allowing critique  and user stories from meeting transcripts and recordings, ensuring accuracy and efficiency.

## Architecture and Implementation

### Architecture Overview

![image](https://github.com/user-attachments/assets/527ec609-e874-4d9e-a015-e7bb3a13ea74)


### Implementation Overview

![image](https://github.com/user-attachments/assets/f0e14ff9-12ad-4d8f-8203-0b4c833f6679)

#### Data Extraction & Ingestion

Data Extraction : Meeting recordings and transcripts will be uploaded by the user through the UI. In the future, these transcripts will be uploaded to a blob storage. Data will be extracted from here.

StorySpinner utilizes a Hybrid Retrieval-Augmented Generation (RAG) approach to enhance the accuracy and relevance of the generated documents. This approach combines the strengths of retrieval-based and generation-based models to produce high-quality outputs.

### Azure AI Studio and Prompt Flow

StorySpinner leverages Azure AI Studio for model training and deployment. The prompt flow is designed to ensure seamless interaction between the user and the system, guiding the user through the process of generating and approving documents.

## Application Overview

StorySpinner accepts meeting transcripts and call recordings as input, generates detailed BRDs, allows for critique and modification, and finally produces user stories once the BRD is approved.

## Technologies Used

- **Python**: Core programming language for implementation.
- **LangGraph/Semantic Kernel**: Used for natural language processing and understanding.
- **Azure DevOps**: For continuous integration and deployment.
- **Streamlit**: For building the user interface.
- **Power Automate**: For approval workflows.

## Target Audience

StorySpinner is designed for project managers, business analysts, and development teams who need to streamline the process of documenting meeting outcomes and generating actionable user stories.

## Conclusion and Future Works

StorySpinner significantly reduces the time and effort required to convert meeting discussions into structured documents. Future enhancements may include integration with more communication platforms, advanced natural language understanding capabilities, and additional customization options for generated documents.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Required Python libraries (listed in `requirements.txt`)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/microsoft/RAG_Hack.git
    cd RAG_Hack/StorySpinner
    ```

2. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

### Usage

1. **Input Meeting Transcript/Recording**:
    - Place your meeting transcript or call recording in the `input` directory.

2. **Generate BRD**:
    - Run the following command to generate the Business Requirement Document:
      ```bash
      python generate_brd.py --input input/meeting_transcript.txt
      ```

3. **Critique and Modify BRD**:
    - The generated BRD will be available in the `output` directory. A designated critique can review and modify the content as needed.

4. **Approve and Generate User Stories**:
    - Once the BRD is approved, run the following command to generate user stories:
      ```bash
      python generate_user_stories.py --input output/approved_brd.txt
      ```

### Example

Here's an example workflow:

1. Place `meeting_transcript.txt` in the `input` directory.
2. Run `generate_brd.py` to create `brd_output.txt` in the `output` directory.
3. The critique reviews and modifies `brd_output.txt`, saving the approved version as `approved_brd.txt`.
4. Run `generate_user_stories.py` to create `user_stories.txt` in the `output` directory.

## Team Member:
1. Manashi Sarkar (https://www.linkedin.com/in/manashi-sarkar-b1692049/)
2. Satyaki Majumdar (https://www.linkedin.com/in/satyaki-majumdar-8602a7118/)
3. Sarbo Mitra (https://www.linkedin.com/in/sarbo-mitra-50338a212/)


## Acknowledgments

- Inspired by the need to streamline the documentation process in project management.
- Special thanks to the Microsoft RAG Hackathon team for their support and guidance.
