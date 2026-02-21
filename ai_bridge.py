import os
from openai import OpenAI

featherless_client = OpenAI(
    base_url="https://api.featherless.ai/v1",
    api_key="rc_94ba2f9e411b3ffaf5c8190eb9c7c1b43670d74b0bb16a08d1ce63b4a66cc5c9"
)

PLANNER = "z-ai/glm-5"
CODER = "deepseek-ai/DeepSeek-V3-2"