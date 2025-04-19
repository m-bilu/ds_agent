import pandas as pd
from typing import Dict
import cohere
from schema import State
import os

co = cohere.Client(os.environ['COHERE_API_KEY'])

def load_data(state: State) -> Dict[str, pd.DataFrame]:
    '''
    load_data() returns the data which is meant to be used by the DS Agent

    Args:
    - filepath: The filepath to the dataset (should end in csv)

    Returns:
    - a dictionary with key 'data', value is a dataframe
    '''
    train = pd.read_csv(state['filepath'] + '/train.csv')
    test = pd.read_csv(state['filepath'] + '/test.csv')
    return {'train' : train, 'test': test}

def generate_python_code(state: State) -> Dict[str, str]:
    '''
    generate_code() returns a string representing a python function, based off of the user's question about the data
    - if the user asks for a histogram on one of the variables
    - if the user asks for a corr map between two variables
        - this function prompts llm to return code representing a make_hist() function, etc.
    '''

    ### Improvement: This prompt should be generated from previous chain-of-thoughts
    prompt=f"""
    You are a data scientist tasked with writing some python code. You have a local variable called 'train' which holds a pandas dataframe.

    Write Python code using the 'train' dataframe to answer the following question: "{state['queries'][-1]}".

    Follow these rules as you write the code:
    - There is a dataframe named 'train' already in scope of your Python code. Do not define it yourself.
    - Do not use any data other than the 'train' dataframe.
    - You should import all libraries needed
    - You should define a variable named 'result' at the end which holds a string containing the final answer for the question.
    
    Example of dataframe stored in local variable 'train': {state['train'].head(3).to_dict()}
    """

    response = co.generate(prompt=prompt, model="command")
    codelines = response.generations[0].text.strip().splitlines()
    if len(codelines) > 2:
        codestart=None
        codeend=None

         # Find first occurrence of "```python"
        for i, line in enumerate(codelines):
            if line.strip() == "```python":
                codestart = i
                break

        # Find first occurrence of "```" after "```python"
        if codestart is not None:
            for j in range(codestart + 1, len(codelines)):
                if codelines[j].strip() == "```":
                    codeend = j
                    break
            
        code = "\n".join(codelines[codestart+1:codeend])
        return {'queryprompts': [prompt], 'code': code}
    else:
        raise Exception(f'Code Response has <= 2 lines: {codelines}')
    

def execute_code(state: State) -> Dict[str, str]:
    '''
    This method exectes the generated python code
    '''
    local_vars = {"train": state["train"]}
    
    try:
        exec(state['code'], globals(), local_vars)
        result = local_vars.get("result", "No result returned.")
    except Exception as e:
        result = f"Error executing code: {str(e)}"
    
    return {"coderesult": [result]}


def summarize_response(state: State) -> Dict[str, str]:
    '''
    Summarize the response using the history and the new calculated answer once code has been executed.
    '''
    
    prompt=f"""
    Consider the following query or queries that was made earlier:

    "{state['queries']}"

    Here is the prompt used to write code to answer this query:

    "{state['queryprompts']}"

    Here is the response you came up with:

    "{state['code']}"

    Here is the code you came up with:

    "{state['coderesult']}"

    Using this context, generate a summary for the user's original query, using the final answer.
    """

    response = co.generate(prompt=prompt, model="command")

    return {'answers': [response.generations[0].text]}
    
    

