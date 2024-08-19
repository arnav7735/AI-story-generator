# from flask import Flask, request, jsonify, send_from_directory
# from transformers import GPT2Tokenizer, GPT2LMHeadModel, pipeline

# app = Flask(__name__)

# # Load the fine-tuned model and tokenizer
# load_dir_location = r"E:\My Projects\Actual Fun Projects\PythonXNode\gagan_finetuned_model"
# model = GPT2LMHeadModel.from_pretrained(load_dir_location)

# load_tokenizer_dir_location = r"E:\My Projects\Actual Fun Projects\PythonXNode\gagan_tokenizer"
# tokenizer = GPT2Tokenizer.from_pretrained(load_tokenizer_dir_location)

# # Initialize the text generation pipeline
# generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

# def generate_story(input_text, iteration):
#     base_max_length = 80
#     current_max_length = base_max_length + (iteration * 15)
    
#     outputs = generator(
#         input_text, 
#         max_length=current_max_length, 
#         num_return_sequences=3, 
#         eos_token_id=tokenizer.eos_token_id,
#         temperature=0.7, 
#         top_k=50, 
#         top_p=0.9, 
#         no_repeat_ngram_size=2, 
#         pad_token_id=tokenizer.pad_token_id
#     )
    
#     return [output['generated_text'] for output in outputs]

# @app.route('/generate', methods=['POST'])
# def generate():
#     try:
#         input_data = request.json
#         input_text = input_data['input_text']
#         iteration = input_data['iteration']
        
#         # Generate story based on the input data
#         results = generate_story(input_text, iteration)
        
#         # Format and return results as JSON
#         output = {
#             "result1": results[0],
#             "result2": results[1],
#             "result3": results[2]
#         }
        
#         return jsonify(output)
    
#     except Exception as e:
#         # Return error message
#         return jsonify({'error': str(e)}), 500

# # Route to serve the static HTML file
# @app.route('/')
# def serve_static_index():
#     return send_from_directory('static', 'index.html')

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)

################################

# from flask import Flask, request, jsonify, send_from_directory
# from transformers import GPT2Tokenizer, GPT2LMHeadModel, pipeline
# import logging

# app = Flask(__name__)

# # Load the fine-tuned model and tokenizer
# load_dir_location = r"E:\My Projects\Actual Fun Projects\PythonXNode\gagan_finetuned_model"
# model = GPT2LMHeadModel.from_pretrained(load_dir_location)

# load_tokenizer_dir_location = r"E:\My Projects\Actual Fun Projects\PythonXNode\gagan_tokenizer"
# tokenizer = GPT2Tokenizer.from_pretrained(load_tokenizer_dir_location)

# # Initialize the text generation pipeline
# generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

# logging.basicConfig(level=logging.DEBUG)

# def generate_story(input_text, iteration, num):
#     base_max_length = 40
#     current_max_length = base_max_length + (iteration * 15)
    
#     outputs = generator(
#         input_text, 
#         max_length=current_max_length, 
#         num_return_sequences=3, 
#         eos_token_id=tokenizer.eos_token_id,
#         temperature=0.7, 
#         top_k=50, 
#         top_p=0.9, 
#         no_repeat_ngram_size=2, 
#         pad_token_id=tokenizer.pad_token_id
#     )
    
#     generated_texts = [output['generated_text'] for output in outputs]
#     logging.debug(f"Generated texts for iteration {iteration}: {generated_texts}")
#     return generated_texts

# @app.route('/generate', methods=['POST'])
# def generate():
#     try:
#         input_data = request.json
#         previous_story = input_data['previous_story']
#         iteration = input_data['iteration']
        
#         # Generate story based on the previous story
#         results = generate_story(previous_story, iteration)
        
#         # Format and return results as JSON
#         output = {
#             "result1": results[0],
#             "result2": results[1],
#             "result3": results[2]
#         }
#         num = num + 80
        
#         return jsonify(output)
    
#     except Exception as e:
#         # Return error message
#         return jsonify({'error': str(e)}), 500

# # Route to serve the static HTML file
# @app.route('/')
# def serve_static_index():
#     return send_from_directory('static', 'index.html')

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)



from flask import Flask, request, jsonify, send_from_directory
from transformers import GPT2Tokenizer, GPT2LMHeadModel, pipeline
import logging

app = Flask(__name__)

# Load the fine-tuned model and tokenizer
load_dir_location = r"E:\My Projects\Actual Fun Projects\PythonXNode\gagan_finetuned_model"
model = GPT2LMHeadModel.from_pretrained(load_dir_location)

load_tokenizer_dir_location = r"E:\My Projects\Actual Fun Projects\PythonXNode\gagan_tokenizer"
tokenizer = GPT2Tokenizer.from_pretrained(load_tokenizer_dir_location)

# Initialize the text generation pipeline
generator = pipeline('text-generation', model=model, tokenizer=tokenizer)

logging.basicConfig(level=logging.DEBUG)

# Global variable to track base_max_length
story_state = {'base_max_length': 40}

def generate_story(input_text, iteration):
    current_max_length = story_state['base_max_length'] # (iteration * 300)#
    
    outputs = generator(
        input_text, 
        max_length=current_max_length, 
        num_return_sequences=3, 
        eos_token_id=tokenizer.eos_token_id,
        temperature=0.7,    
        top_k=50, 
        top_p=0.9, 
        no_repeat_ngram_size=2, 
        pad_token_id=tokenizer.pad_token_id
    )
    
    generated_texts = [output['generated_text'] for output in outputs]
    logging.debug(f"Generated texts for iteration {iteration}: {generated_texts}")
    
    # Update base_max_length for the next iteration
    story_state['base_max_length'] *= 2
    
    return generated_texts

@app.route('/generate', methods=['POST'])
def generate():
    try:
        input_data = request.json
        previous_story = input_data['previous_story']
        iteration = input_data['iteration']
        
        # Generate story based on the previous story
        results = generate_story(previous_story, iteration)
        
        # Format and return results as JSON
        output = {
            "result1": results[0],
            "result2": results[1],
            "result3": results[2]
        }
        
        return jsonify(output)
    
    except Exception as e:
        # Return error message
        return jsonify({'error': str(e)}), 500

# Route to serve the static HTML file
@app.route('/')
def serve_static_index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
