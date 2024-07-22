"""OpenAI configs"""
import dotenv


OPENAI_APITOKEN = dotenv.get_key('.env', 'OPENAI_APITOKEN')
OPENAI_MODELNAME = dotenv.get_key('.env', 'OPENAI_MODELNAME')

