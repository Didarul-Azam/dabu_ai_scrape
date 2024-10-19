# gemini.py

import time
import google.generativeai as genai

from google.generativeai.types import HarmCategory, HarmBlockThreshold
from tenacity import retry, stop_after_attempt, wait_exponential





class Gemini:
    safety_settings = dict.fromkeys(
        [
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            HarmCategory.HARM_CATEGORY_HARASSMENT,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT
        ],
        HarmBlockThreshold.BLOCK_NONE
    )
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "application/json"
    }

    def __init__(self):
        genai.configure(api_key='AIzaSyDK8Tv19FasEoY9JirhKtgKDRhJ2ATaSR8')
        self.set_model('gemini-1.5-flash-latest')

    def set_model(self, name):
        self.model = genai.GenerativeModel(model_name=name, generation_config=self.generation_config,
                                           safety_settings=self.safety_settings)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_content(self, prompt, files=None, max_timeout=2000, safety_settings=True):
        params = [prompt]
        if files:
            params = [*files, prompt]
        return self.model.generate_content(params, request_options={"timeout": max_timeout},
                                           safety_settings=self.safety_settings if safety_settings else None)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def upload_file(self, file_path):
        
        file_obj = genai.upload_file(file_path)
        return self._check_file_state(file_obj)

    @staticmethod
    def _check_file_state(file_obj):
        while file_obj.state.name == "PROCESSING":
            time.sleep(10)
            file_obj = genai.get_file(file_obj.name)
        if file_obj.state.name == "FAILED":
            raise ValueError(file_obj.state.name)
        return file_obj


gemini = Gemini()
