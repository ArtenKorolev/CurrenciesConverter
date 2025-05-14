from os import getenv
from dotenv import load_dotenv


load_dotenv()

EXCHANGERATE_API_KEY=str(getenv('EXCHANGERATE_API_KEY'))
