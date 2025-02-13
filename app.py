from flask import Flask, render_template, request, send_file, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Global variables to store the current state
current_qa_pairs = []
current_index = 0
kept_pairs = []

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global current_qa_pairs, current_index, kept_pairs
    
    if 'file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400

    # Reset global states
    current_qa_pairs = []
    current_index = 0
    kept_pairs = []
    
    # Read and parse the JSONL file
    for line in file:
        data = json.loads(line)
        conversations = data['conversations']
        
        # Extract QA pairs
        for i in range(len(conversations)):
            if conversations[i]['from'] == 'human' and i + 1 < len(conversations) and conversations[i + 1]['from'] == 'gpt':
                qa_pair = {
                    'question': conversations[i]['value'],
                    'answer': conversations[i + 1]['value']
                }
                current_qa_pairs.append(qa_pair)
    
    return jsonify({
        'total': len(current_qa_pairs),
        'current': current_qa_pairs[current_index] if current_qa_pairs else None
    })

@app.route('/update_qa', methods=['POST'])
def update_qa():
    global current_qa_pairs, current_index
    
    data = request.json
    if current_index < len(current_qa_pairs):
        current_qa_pairs[current_index]['question'] = data.get('question', '')
        current_qa_pairs[current_index]['answer'] = data.get('answer', '')
        return jsonify({'success': True})
    return jsonify({'success': False}), 400

@app.route('/next', methods=['POST'])
def next_pair():
    global current_index
    
    action = request.json.get('action')  # 'keep' or 'delete'
    
    if action == 'keep' and current_index < len(current_qa_pairs):
        kept_pairs.append(current_qa_pairs[current_index])
    
    current_index += 1
    
    if current_index >= len(current_qa_pairs):
        return jsonify({'finished': True})
    
    return jsonify({
        'qa_pair': current_qa_pairs[current_index],
        'progress': f"{current_index + 1}/{len(current_qa_pairs)}"
    })

@app.route('/save', methods=['POST'])
def save_filtered():
    # Create output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"filtered_qa_{timestamp}.jsonl"
    
    # Convert kept pairs back to original format
    output_data = []
    for pair in kept_pairs:
        conversations = [
            {"from": "system", "value": "You are a helpful AI assistant."},
            {"from": "human", "value": pair['question']},
            {"from": "gpt", "value": pair['answer']}
        ]
        output_data.append({"conversations": conversations})
    
    # Write to file
    with open(output_filename, 'w') as f:
        for item in output_data:
            f.write(json.dumps(item) + '\n')
    
    return jsonify({'filename': output_filename})

if __name__ == '__main__':
    app.run(debug=True)
