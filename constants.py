import os

# Define configuration constants
URL = os.getenv("FUNCTION_URL")
ADMIN_CHAT_ID = int(os.getenv('ADMIN_CHAT_ID'))
TOKEN = os.getenv('BOT_TOKEN')  # nosec B105

