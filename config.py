import os

from dotenv import load_dotenv
load_dotenv()


CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
BOT_TOKEN = os.environ['BOT_TOKEN']

# Bot settings
COMMAND_PREFIX = os.environ['COMMAND_PREFIX']
HELP_COMMAND = os.getenv('HELP_COMMAND', 'help')
