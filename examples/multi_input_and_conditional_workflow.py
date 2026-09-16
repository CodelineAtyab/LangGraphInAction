from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class SharedStateDict(TypedDict):
    name: str
    operation: str
    values: list[int]
    result: int


def update_greet_message(state: SharedStateDict) -> SharedStateDict:
    state["name"] = "Assalam O Alikum! " + state["name"]
    return state


def route_based_on_operation(state: SharedStateDict):
    if state["operation"] == "*":
        return "peform_mulitplication_path"
    elif state["operation"] == "+":
        return "perform_addition_path"


def peform_mulitplication(state: SharedStateDict) -> SharedStateDict:
    state["result"] = 10
    return state


def perform_addition(state: SharedStateDict) -> SharedStateDict:
    state["result"] = 20
    return state


current_workflow = StateGraph(SharedStateDict)

current_workflow.add_node(node="update_greet_message", action=update_greet_message)

# Start Node
current_workflow.add_edge(start_key=START, end_key="update_greet_message")

current_workflow.add_node(node="peform_mulitplication", action=peform_mulitplication)
current_workflow.add_node(node="perform_addition", action=perform_addition)
current_workflow.add_conditional_edges(
    source="update_greet_message",
    path=route_based_on_operation,
    path_map={
        "peform_mulitplication_path" : "peform_mulitplication",
        "perform_addition_path" : "perform_addition"
    }
)

# End Node 
current_workflow.add_edge(start_key="peform_mulitplication", end_key=END)
current_workflow.add_edge(start_key="perform_addition", end_key=END)

compiled_graph_workflow = current_workflow.compile()

print(compiled_graph_workflow.get_graph().draw_ascii())
print(compiled_graph_workflow.invoke({"name": "Atyab", "operation": "+"}))