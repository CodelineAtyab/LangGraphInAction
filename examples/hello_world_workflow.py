from typing import TypedDict
from langgraph.graph import StateGraph


class AgentState(TypedDict):
    message: str


def greet(shared_state: AgentState) -> AgentState:
    return {"message": "Greetings! " + shared_state["message"]}


graph_workflow = StateGraph(AgentState)
graph_workflow.add_node("greet_node", greet)
graph_workflow.set_entry_point("greet_node")
graph_workflow.set_finish_point("greet_node")
app = graph_workflow.compile()

app.get_graph().print_ascii()

print(app.invoke({"message": "Atyab"}))