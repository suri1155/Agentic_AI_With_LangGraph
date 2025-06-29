import os
from typing import Literal, Any, Optional

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

from utils.config_loader import load_config


class ConfigLoader:
    def __init__(self):
        print("Config Loaded...")
        self.config = load_config()

    def __getitem__(self, key):
        return self.config[key]


class ModelLoader(BaseModel):
    model_provider: Literal["openai", "groq"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()

    class Config:
        arbitrary_types_allowed = True
    
    def load_llm(self):
        if self.model_provider == "openai":
            print("Loading OpenAI model...")
            open_api_key = os.getenv("OPENAI_API_KEY")
            model_name = self.config["llm"]["openai"]["model_name"]
            llm = ChatOpenAI(
                model_name=model_name,
                openai_api_key=open_api_key
            )
        elif self.model_provider == "groq":
            print("Loading Groq model...")
            groq_api_key = os.getenv("GROQ_API_KEY")
            model_name = self.config["llm"]["groq"]["model_name"]
            llm = ChatGroq(
                model_name=model_name,
                groq_api_key=groq_api_key
            )
            
        else:
            raise ValueError(f"Unsupported model provider: {self.model_provider}")
        return llm



