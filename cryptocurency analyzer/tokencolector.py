"""
 Contains the classes for manging diferent cryptographic sensetive information.

Contents:
    Token Colector class

Returns:
    str: Return string representation of the API key.
"""

import os
from dotenv import load_dotenv


class TokenColector:
    """
     Standard way to interact with the API server
     through the token

    Loads the token from the environment files located in the path specified

    args: file_name: full or relative name of the *.env file (with path)
    """    """"""

    def __init__(self, token_name: str, file_name: str) -> None:
        self.token_name = token_name
        # load_dotenv(dotenv_path="./API.env")
        # TOKEN = "VANTAGE"
        # self.api_key = os.environ[TOKEN]
        load_dotenv(dotenv_path=file_name)
        self.api_key = os.environ[self.token_name]

    def get_api_key(self) -> str:
        """
        get_api_key Method to retrieve the API key

        returns: string formated API key
        """        """"""
        return self.api_key
