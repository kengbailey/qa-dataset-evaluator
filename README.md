# QA Dataset Evaluator

A web-based tool for evaluating, filtering, and editing question-answer datasets in JSONL format. This tool helps in cleaning and curating QA datasets by providing an intuitive interface to review, edit, and filter QA pairs.

## Features

- **File Upload**: Upload JSONL files containing question-answer pairs
- **Interactive Review**: Review QA pairs one at a time with a clean interface
- **Edit Capability**: Edit questions and answers directly in the interface
- **Keep/Delete**: Choose to keep or remove specific QA pairs
- **Progress Tracking**: Track progress through the dataset
- **Export**: Export the filtered dataset with timestamp in JSONL format

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kengbailey/qa-dataset-evaluator.git
cd qa-dataset-evaluator
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Use the interface to:
   - Upload a JSONL file containing QA pairs
   - Review each QA pair
   - Edit questions or answers if needed
   - Choose to keep or delete each pair
   - Export the filtered dataset when finished

## Input File Format

The tool expects JSONL files with the following structure:

```json
{
  "conversations": [
    {"from": "system", "value": "You are a helpful AI assistant."},
    {"from": "human", "value": "Your question here"},
    {"from": "gpt", "value": "Your answer here"}
  ]
}
```

Each line in the JSONL file should contain a separate conversation object.

## Output Format

The filtered dataset will be saved as a JSONL file with the name format: `filtered_qa_YYYYMMDD_HHMMSS.jsonl`

The output maintains the same structure as the input format, including only the kept QA pairs.

## Requirements

- Python 3.x
- Flask
- Additional dependencies listed in `requirements.txt`
