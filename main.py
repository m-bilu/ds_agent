from langgraph.graph import StateGraph
from ds_tools import load_data, generate_python_code, execute_code, summarize_response
import kagglehub
import sys

from schema import State

graph = StateGraph(State)

graph.add_node("load_data", load_data)
graph.add_node("generate_python_code", generate_python_code)
graph.add_node("execute_code", execute_code)
graph.add_node("summarize_response", summarize_response)


graph.add_edge("load_data", "generate_python_code")
graph.add_edge("generate_python_code", "execute_code")
graph.add_edge("execute_code", "summarize_response")

graph.set_entry_point("load_data")
eda_assistant = graph.compile()

if __name__ == '__main__':
    # Example execution
    path = kagglehub.dataset_download("sidharth178/car-prices-dataset")
    query = "What is the average price of a car?" if len(sys.argv) < 2 else sys.argv[1]

    print(query)
    result = eda_assistant.invoke(State(filepath=path, queries=[query]))

    print(result['code'])
    print(result['coderesult'])
    print(result['answers'])
