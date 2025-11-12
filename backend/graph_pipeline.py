from copy import deepcopy
import json
from copy import deepcopy
from state_schema import PipelineState
from langgraph.graph import StateGraph, END, START
from langchain_core.runnables import RunnableParallel
from nodes.nodes import (
    ingestion_node,   
    notemaking_node,
    concept_extraction_node,
    tag_generator_node,
    websearch_node,
    style_rewriter_node,
)

# -------------------------------
# Setup: Parallel agent execution
# -------------------------------
parallel_agents = RunnableParallel(
    tag_generation=tag_generator_node,
    web_search=websearch_node,
    style_rewrite=style_rewriter_node,
)


# -------------------------------
# Helper: Deep merge dictionaries
# -------------------------------
def deep_merge_dict(base: dict, update: dict) -> dict:
    """Recursively merge two dicts without losing nested keys."""
    for k, v in update.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            base[k] = deep_merge_dict(base[k], v)
        else:
            base[k] = v
    return base


def parallel_merge_node(state: PipelineState) -> PipelineState:
    print("---RUNNING PARALLEL AGENTS---")
    outputs = parallel_agents.invoke(state)

    new_state = deepcopy(state)

    for agent_name, result in outputs.items():
        print(f"\n[MERGING OUTPUT] from agent: {agent_name}")
        try:
            print(json.dumps(result, indent=2, default=str))
        except Exception:
            print("(non-serializable output hidden)")
        new_state = deep_merge_dict(new_state, result)

    return new_state


# -------------------------------
# Pipeline assembly
# -------------------------------
def build_pipeline():
    graph = StateGraph(PipelineState)

    graph.add_node("ingestion", ingestion_node)
    graph.add_node("notemaking", notemaking_node)
    graph.add_node("concept_extraction", concept_extraction_node)
    graph.add_node("parallel_generation", parallel_merge_node)

    graph.add_edge("ingestion", "notemaking")
    graph.add_edge("notemaking", "concept_extraction")
    graph.add_edge("concept_extraction", "parallel_generation")
    graph.add_edge("parallel_generation", END)

    graph.set_entry_point("ingestion")
    return graph.compile()


workflow = build_pipeline()
