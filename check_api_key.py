import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Print debug information
print(f"API key found: {'Yes' if api_key else 'No'}")
print(f"API key first 10 characters: {api_key[:10]}..." if api_key else "No API key found")

# Check API key validity using a simple models list request
url = "https://api.openai.com/v1/models"
headers = {
    "Authorization": f"Bearer {api_key}"
}

try:
    print("\nAttempting to list available models...")
    response = requests.get(url, headers=headers)
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        print("API key is valid! Here are the available models:")
        models = response.json()["data"]
        for model in models[:5]:  # Show only first 5 models
            print(f"- {model['id']}")
        print("...")
    else:
        print(f"API key validation failed. Error: {response.text}")
        
        # Check if it's a quota issue
        if response.status_code == 429:
            print("\nThis appears to be a quota issue. Here are some possible solutions:")
            print("1. Check your OpenAI account billing status at https://platform.openai.com/account/billing")
            print("2. Make sure your payment method is valid")
            print("3. If you're using a free tier, you might have exhausted your free credits")
            print("4. Contact OpenAI support if you believe this is an error")
        
        # Check if it's an authentication issue
        elif response.status_code == 401:
            print("\nThis appears to be an authentication issue. Here are some possible solutions:")
            print("1. Make sure your API key is correct")
            print("2. Check if your API key has been revoked")
            print("3. Verify that you're using the correct type of API key")
            print("4. Generate a new API key at https://platform.openai.com/api-keys")
            
            # Check if the API key format is unusual
            if not api_key.startswith("sk-") or "proj" in api_key:
                print("\nYour API key format looks unusual:")
                print("- Standard OpenAI API keys start with 'sk-' followed by a string of characters")
                print("- Your key starts with 'sk-proj-', which might indicate it's from a different service")
                print("- Please verify you're using an API key from https://platform.openai.com/api-keys")
                
except Exception as e:
    print(f"Error during API key validation: {str(e)}")
