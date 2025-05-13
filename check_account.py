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

# Check API key validity using the organization endpoint
url = "https://api.openai.com/v1/organizations"
headers = {
    "Authorization": f"Bearer {api_key}"
}

try:
    print("\nAttempting to get organization info...")
    response = requests.get(url, headers=headers)
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        print("Organization info retrieved successfully!")
        org_data = response.json()
        print(f"Organization data: {org_data}")
    else:
        print(f"Failed to retrieve organization info. Error: {response.text}")
        
except Exception as e:
    print(f"Error during API request: {str(e)}")

# Check billing info
url = "https://api.openai.com/dashboard/billing/subscription"
try:
    print("\nAttempting to get billing info...")
    response = requests.get(url, headers=headers)
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        print("Billing info retrieved successfully!")
        billing_data = response.json()
        print(f"Billing data: {billing_data}")
    else:
        print(f"Failed to retrieve billing info. Error: {response.text}")
        
except Exception as e:
    print(f"Error during API request: {str(e)}")

print("\nPossible reasons for quota issues:")
print("1. Your free trial credits have been exhausted")
print("2. Your account doesn't have a valid payment method")
print("3. You've reached your usage limit for the current billing period")
print("4. Your account might be suspended or restricted")
print("\nRecommended actions:")
print("1. Check your account status at https://platform.openai.com/account/billing")
print("2. Add a payment method if you haven't already")
print("3. Contact OpenAI support if you believe this is an error")
print("4. Create a new API key and try again")
