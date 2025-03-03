import langgraph
from ds_tools import load_data, generate_python_code, execute_code
import kagglehub

graph = langgraph.Graph()

graph.add_node("load_data", load_data)
graph.add_node("generate_python_code", generate_python_code)
graph.add_node("execute_code", execute_code)

graph.add_edge("load_data", "generate_python_code")
graph.add_edge("generate_python_code", "execute_code")

graph.set_entry_point("load_data")
eda_assistant = graph.compile()

# Example execution
# Download latest version
path = kagglehub.dataset_download("sidharth178/car-prices-dataset")
query = "What is the average price of a car?"
result = eda_assistant.invoke({"file_path": path, "query": query})

print(result["answer"])
