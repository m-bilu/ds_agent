import pandas as pd
from typing import Dict
import cohere

co = cohere.Client("YOUR_COHERE_API_KEY")

def load_data(filepath: str) -> Dict[str, pd.DataFrame]:
    '''
    load_data() returns the data which is meant to be used by the DS Agent

    Args:
    - filepath: The filepath to the dataset (should end in csv)

    Returns:
    - a dictionary with key 'data', value is a dataframe
    '''
    df = pd.read_csv(filepath)
    return {'data' : df}

def generate_python_code(data: Dict[str, pd.DataFrame], query: str):
    '''
    generate_code() returns a string representing a python function, based off of the user's question about the data
    - if the user asks for a histogram on one of the variables
    - if the user asks for a corr map between two variables
        - this function prompts llm to return code representing a make_hist() function, etc.
    '''
    prompt=f"""
    Given a dataset in Pandas DataFrame format, write a Python function to answer the following query: '{query}'.
    The function should:
    - Use the DataFrame named 'df'
    - Return the result in a format suitable for display
    - Avoid unnecessary complexity
    
    Example dataset: {data['data'].head(3).to_dict()}
    """

    response = co.generate(prompt=prompt, model="command")
    code = response.generations[0].text.strip()
    
    return {"code": code}

def execute_code(data: Dict[str, pd.DataFrame], code: Dict[str, str]) -> Dict[str, str]:
    '''
    This method exectes the generated python code
    '''
    df = data["data"]
    local_vars = {"df": df}
    
    try:
        exec(code, {}, local_vars)
        result = local_vars.get("result", "No result returned.")
    except Exception as e:
        result = f"Error executing code: {str(e)}"
    
    return {"answer": result}

