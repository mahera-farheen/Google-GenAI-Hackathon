import os
import io
import base64
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from PIL import Image
import json

# Initialize the Flask application
app = Flask(__name__, template_folder='templates')
CORS(app) # This will allow cross-origin requests

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
text_model = genai.GenerativeModel('gemini-1.5-flash')
multimodal_model = genai.GenerativeModel('gemini-1.5-flash')
# Create a GenerativeModel for text-to-audio using the correct, up-to-date model.
audio_model = genai.GenerativeModel(model_name="gemini-2.5-flash-preview-tts")
# To maintain chat history for the chat model
chat_history = []
chat_session = multimodal_model.start_chat(history=chat_history)

def handle_error(e):
    """A helper function to handle API errors and return a JSON response."""
    print(f"An error occurred: {e}")
    return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    """Serves the main HTML page for the application."""
    return render_template('index.html')

@app.route('/generate_text', methods=['POST'])
def generate_text():
    """
    Handles text generation requests.
    Receives a prompt and returns the generated text.
    """
    try:
        data = request.json
        prompt = data.get('prompt')
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400
        
        # Call the text generation model
        response = text_model.generate_content(prompt)
        
        return jsonify({'text': response.text})
    except Exception as e:
        return handle_error(e)

@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    """
    Handles image analysis and background removal requests.
    Receives an image and a prompt, then returns the analysis and a
    simulated "polished" image with a transparent background.
    """
    try:
        # Get the image and prompt from the form data
        image_file = request.files.get('image')
        prompt = request.form.get('prompt')
        
        if not image_file or not prompt:
            return jsonify({'error': 'Missing image or prompt'}), 400
        
        # Read the image file and convert it to a PIL Image
        img = Image.open(image_file.stream)
        
        # Generate a response based on the image and prompt
        analysis_response = multimodal_model.generate_content([prompt, img])
        analysis_text = analysis_response.text

        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        polished_image = Image.new('RGBA', img.size, (0, 0, 0, 0)) # Create a transparent image
        
        # Convert the new polished image to a base64 string
        buffered = io.BytesIO()
        polished_image.save(buffered, format="PNG")
        polished_image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return jsonify({
            'analysis': analysis_text,
            'polished_image': polished_image_base64
        })
    except Exception as e:
        return handle_error(e)

@app.route('/chat', methods=['POST'])
def chat():
    """
    Manages the conversational chat session.
    Receives a user message, updates the chat history, and returns the model's response.
    """
    try:
        data = request.json
        user_message = data.get('message')
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # Send the user message to the chat session and get the response
        response = chat_session.send_message(user_message)

        return jsonify({'text': response.text})
    except Exception as e:
        return handle_error(e)

@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    """
    Generates audio from text using the text-to-audio model.
    Receives text, generates an audio file, and returns it as a base64 string.
    """
    try:
        data = request.json
        prompt = data.get('prompt')
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400

        # Call the text-to-audio model with streaming enabled
        response = audio_model.generate_content(
            prompt,
            stream=True,
            generation_config={"response_modalities": ["AUDIO"]}
        )
        audio_buffer = io.BytesIO()
        for chunk in response:
            if hasattr(chunk, 'audio_data'):
                audio_buffer.write(chunk.audio_data)
        audio_data = audio_buffer.getvalue()
        if not audio_data:
            return jsonify({'error': 'Received empty audio data from the API. Please try again or check your API key.'}), 500

        return jsonify({
            'audio': base64.b64encode(audio_data).decode('utf-8'),
            'mimeType': 'audio/L16;rate=16000' 
              })
    except Exception as e:
        return handle_error(e)
if __name__ == '__main__':
    app.run(debug=True)
