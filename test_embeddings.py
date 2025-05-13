import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Print debug information
print(f"API key found: {'Yes' if api_key else 'No'}")
print(f"API key first 10 characters: {api_key[:10]}..." if api_key else "No API key found")

# Initialize the OpenAI client
client = openai.OpenAI(api_key=api_key)

try:
    print("\nAttempting to create embeddings...")
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input="Hello, world!"
    )
    
    print("Embeddings created successfully!")
    print(f"Embedding dimensions: {len(response.data[0].embedding)}")
    print(f"First 5 values: {response.data[0].embedding[:5]}")
    
except Exception as e:
    import traceback
    print(f"Full error details: {traceback.format_exc()}")
    print(f"Error: {str(e)}")
