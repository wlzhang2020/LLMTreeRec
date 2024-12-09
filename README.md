# LLMTreeRec

## Introduction

This is the code repository for paper "LLMTreeRec: A Tree-based Large Language Model Framework for Cold-start Recommendation"

## Setup

### 1. Obtain OpenAI API Keys

Before running the project, you need to configure the OpenAI API keys in the `OpenAILLM.py` file. Replace the placeholder values with your actual OpenAI API details.

Replace the placeholder strings with your own values like this:

```python
os.environ["OPENAI_API_VERSION"] = "your_openai_api_version"
os.environ["AZURE_OPENAI_API_KEY"] = "your_azure_openai_api_key"
os.environ["AZURE_OPENAI_ENDPOINT"] = "your_azure_openai_endpoint"
```
or
```python
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"
os.environ["BASE_URL"] = "your_openai_base_url"
```

### 2. Running the Code

Once the API keys are properly set, you can run the main script:

```bash
python main.py
```