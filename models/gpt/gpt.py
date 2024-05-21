import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class GptModel:
    def __init__(self, engine="gpt-3.5-turbo"):
        self.client = OpenAI()
        self.engine = engine

    def query(self, context="", question="", max_tokens=150, temperature=0.7, debug=False):
        try:
            messages = [
                {"role": "system", "content": context},
                {"role": "user", "content": question},
            ]

            response = self.client.chat.completions.create(
                model=self.engine,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            response_content = response.choices[0].message.content

            if debug:
                print("Prompt:", context+"\n"+question)
                print("Response:", response_content)
                print("----------")

            return response_content
        except Exception as e:
            if debug:
                print("Error during query:", str(e))
            return [str(e)]



if __name__ == "__main__":
    model = GptModel()
    prompts = (
        "Tell me something interesting about AI."
    )
    response = model.query(prompts, max_tokens=400, temperature=0)
    print(response)