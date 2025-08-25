import os
import pyttsx3
import google.generativeai as genai

# Initialize Gemini API
genai.configure(api_key= "your_key")
model = genai.GenerativeModel("gemini-1.5-pro")


# Function to generate learning content based on topics and time
def generate_learning_text(topics, minutes):
    prompt = (
        f"Create an engaging {minutes * 60} seconds (around {minutes} minute) educational audio snippet "
        f"on the following topics: {topics}. Keep it conversational and easy to follow."
    )
    response = model.generate_content(prompt)
    return response.text

# Convert text to speech and save as mp3
def text_to_speech(text, filepath):
    engine = pyttsx3.init()
    engine.save_to_file(text, filepath)
    engine.runAndWait()

# Create audio snippet by generating text and converting it to speech
def create_audio_snippet(topics, minutes, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate the filename - using safe filename characters
    safe_topics = topics.replace(',', '').replace(' ', '_')
    filename = f"{safe_topics}_{minutes}min.mp3"
    filepath = os.path.join(output_dir, filename)

    # Generate learning content
    text = generate_learning_text(topics, minutes)

    # Convert text to speech and save it as an mp3 file
    text_to_speech(text, filepath)
    
    # Return just the filename - the static folder path will be handled by url_for
    return filename, f"Generating {minutes} minutes of learning snippets on the topics: {topics}"

