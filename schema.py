'''
This file outlines the different schemas used throughout the agent.
'''

from typing import TypedDict, List, Annotated
import pandas as pd

def add(a, b):
    return a + b

class State(TypedDict):
    queries: Annotated[List[str], add]
    queryprompts: Annotated[List[str], add]
    filepath: str
    train: pd.DataFrame
    test: pd.DataFrame
    code: str
    coderesult: str
    answers: Annotated[List[str], add]

