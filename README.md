# StorySpinner

StorySpinner is an innovative tool designed to transform meeting transcripts and call recordings into comprehensive Business Requirement Documents (BRDs) and user stories. This tool streamlines the documentation process, ensuring that all critical details from meetings are captured and converted into actionable insights.

## Features

- **Transcript/Recording Input**: Accepts meeting transcripts and call recordings as input.
- **BRD Generation**: Automatically generates detailed Business Requirement Documents from the input.
- **Content Critique**: Allows a designated critique to review and modify the BRD content.
- **User Story Generation**: Once the BRD is approved, generates user stories for development teams to work upon.

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

## Contributing

We welcome contributions! Please read our contributing guidelines for more details.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the need to streamline the documentation process in project management.
- Special thanks to the Microsoft RAG Hackathon team for their support and guidance.

