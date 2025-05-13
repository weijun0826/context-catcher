import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Print debug information (remove in production)
print(f"API key found: {'Yes' if api_key else 'No'}")
print(f"API key first 10 characters: {api_key[:10]}..." if api_key else "No API key found")

# Initialize the OpenAI client
client = openai.OpenAI(api_key=api_key)

# Example function to use the OpenAI API
def generate_text(prompt):
    try:
        print("Attempting to call OpenAI API...")
        # Try with GPT-3.5-turbo model
        print("Using model: gpt-3.5-turbo")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        return response.choices[0].message.content
    except Exception as e:
        import traceback
        print(f"Full error details: {traceback.format_exc()}")
        return f"Error: {str(e)}"

# Test the API connection
if __name__ == "__main__":
    if api_key:
        print("API key loaded successfully!")

        # Test with a simple prompt
        prompt = "Hello, how are you today?"
        print(f"\nPrompt: {prompt}")
        print(f"Response: {generate_text(prompt)}")
    else:
        print("Error: API key not found. Please check your .env file.")
