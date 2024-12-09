from openai import OpenAI, AzureOpenAI
import os

# os.environ["OPENAI_API_VERSION"] = "OPENAI_API_VERSION"
# os.environ["AZURE_OPENAI_API_KEY"] = "AZURE_OPENAI_API_KEY"
# os.environ["AZURE_OPENAI_ENDPOINT"] = "AZURE_OPENAI_ENDPOINT"
#
# os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"
# os.environ["BASE_URL"] = "BASE_URL"

class OpenAILLM:
    def __init__(self, prompt):
        self.prompt = prompt
        self.messages = [{"role": "system", "content": self.prompt}]
        if "AZURE_OPENAI_API_KEY" in os.environ and os.environ["AZURE_OPENAI_API_KEY"]:
            self.client = AzureOpenAI()
        else:
            self.client = OpenAI()

    def ask(self, question):
        # Ask a question and get response from ChatGPT
        self.messages.append({"role": "user", "content": question})

        response = self.client.chat.completions.create(
            model="gpt-35-turbo",
            messages=self.messages,
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
        )
        message = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": message})
        return message

    def remain_fisrtKRound(self, k):
        # Keep only the first K rounds of conversation
        self.messages = self.messages[:1 + 2 * k]

    def generate(self, question, round):
        # Ask ChatGPT without retrying, return result immediately
        self.remain_fisrtKRound(round - 1)
        self.messages.append({"role": "user", "content": question})
        print(self.messages)
        response = self.client.chat.completions.create(
            model="gpt-35-turbo",
            messages=self.messages,
            temperature=0.5,
            max_tokens=1024,
            top_p=1
        )
        print(response)
        message = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": message})
        return message
