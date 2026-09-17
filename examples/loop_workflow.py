from pathlib import Path
from typing import TypedDict

from langchain_core.runnables.graph import NodeStyles
from langgraph.graph import END, START, StateGraph


class SharedStateDict(TypedDict):
    name: str
    operation: str
    values: list[int]
    curr_values_index: int
    result: int


def update_greet_message(state: SharedStateDict) -> SharedStateDict:
    state["name"] = "Assalam O Alikum! " + state["name"]
    state["result"] = 0 if state["operation"] in ["+", "-"] else 1
    state["curr_values_index"] = 0
    return state


def route_based_on_operation(state: SharedStateDict):
    if state["operation"] == "*":
        return "peform_mulitplication_path"
    elif state["operation"] == "+":
        return "perform_addition_path"


def peform_mulitplication(state: SharedStateDict) -> SharedStateDict:
    state["result"] = state["result"] * state["values"][state["curr_values_index"]]
    state["curr_values_index"] += 1
    return state


def perform_addition(state: SharedStateDict) -> SharedStateDict:
    state["result"] = state["result"] + state["values"][state["curr_values_index"]]
    state["curr_values_index"] += 1
    return state


def should_continue_calculation(state: SharedStateDict):
    if state["curr_values_index"] < len(state["values"]):
        return "continue_calculation_path"
    else:
        return "end_calculation_path"


current_workflow = StateGraph(SharedStateDict)

current_workflow.add_node(node="update_greet_message", action=update_greet_message)

# Start Node
current_workflow.add_edge(start_key=START, end_key="update_greet_message")

# Empty Node to Jump to
current_workflow.add_node(node="prep_for_calculation", action=lambda state: state)
current_workflow.add_edge(start_key="update_greet_message", end_key="prep_for_calculation")

current_workflow.add_node(node="peform_mulitplication", action=peform_mulitplication)
current_workflow.add_node(node="perform_addition", action=perform_addition)
current_workflow.add_conditional_edges(
    source="prep_for_calculation",
    path=route_based_on_operation,
    path_map={
        "peform_mulitplication_path" : "peform_mulitplication",
        "perform_addition_path" : "perform_addition"
    }
)

current_workflow.add_conditional_edges(
    source="perform_addition",
    path=should_continue_calculation,
    path_map={
        "continue_calculation_path": "prep_for_calculation",
        "end_calculation_path": END
    }
)

current_workflow.add_conditional_edges(
    source="peform_mulitplication",
    path=should_continue_calculation,
    path_map={
        "continue_calculation_path": "prep_for_calculation",
        "end_calculation_path": END
    }
)

compiled_graph_workflow = current_workflow.compile()

print(compiled_graph_workflow.get_graph().draw_ascii())

syntax = compiled_graph_workflow.get_graph().draw_mermaid(
    node_colors=NodeStyles(
        default="line-height:1.2",
        first="fill-opacity:0",
        last="stroke-width:2px",
    )
)
Path("examples/loop_workflow_mermaid.md").write_text(
    f"```mermaid\n{syntax}\n```\n",
    encoding="utf-8",
)

print(compiled_graph_workflow.invoke({"name": "Atyab", "operation": "*", "values": [1, 2, 3, 4, 5]}))