import openai
import json
import os
import re
import tempfile


from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']



SYSTEM_MESSAGE = """
  You consider your self as a civil engineer and your Task is to create a python funtion for autocad Using the `pyautocad` python library.
"""
TEMP_FILE_NAME = "temp.py"


class AutoCad_Code_OpenApi:

  def __init__(self):
    self.message_prompt = [
      {
        "role": "system",
        "content": SYSTEM_MESSAGE
      }
    ]

  
  def _add_prompt_to_message(self, prompt, role: str):
    self.message_prompt.append({
      "role": role,
      "content": prompt
    })


  def _get_completion_from_messages(self, messages, model="gpt-3.5-turbo", temperature=0):
      response = openai.ChatCompletion.create(
            model=model,
            messages=self.message_prompt,
            temperature=temperature, # this is the degree of randomness of the model's output
          )
      tempVal = {
        "role": "assistant",
        "content": "Sure! Here's a simple \"Hello, World!\" program in Python:\n\n```python\nprint(\"Hello, World!\")\n```\n\nYou can run this code in any Python environment, such as the Python interpreter or an integrated development environment (IDE). When you run the code, it will display the message \"Hello, World!\" in the console or output window."
      }
      print(str(response.choices[0].message))
      return response.choices[0].message["content"]

  def getCodeFromPrompt(self, prompt: str):
    self._add_prompt_to_message(prompt, "user")
    response = self._get_completion_from_messages(self.message_prompt)
    self._add_prompt_to_message(response, "assistant")
    return self._extract_code_from_string(response)
    

  def _extract_code_from_string(self, response):
    try:
      python_code = self._extract_python_code_from_api_response(response)
      temp = self._save_python_code_to_file(python_code, TEMP_FILE_NAME)
      return temp
    except:
      temp = self._save_python_code_to_file(response, TEMP_FILE_NAME)
      return temp
    
  def _extract_python_code_from_api_response(self, api_response):
    """Extracts Python code from an API response.
    Returns:
        A string containing the Python code.
    """

    python_code_regex = r"`python\n(.*?)\n`"
    python_code = re.findall(python_code_regex, api_response)[0]
    return python_code

  def _save_python_code_to_file(self, python_code, file_name):
    """Saves Python code to a file.
    Args:
        python_code: The Python code.
        file_name: The name of the file to save the code to.
    """

    with open(file_name, "w") as f:
        f.write(python_code)
    return file_name


autoCad_Code_OpenApi = AutoCad_Code_OpenApi()
response = autoCad_Code_OpenApi.getCodeFromPrompt("write a 2 sum function in python")
print(response)
