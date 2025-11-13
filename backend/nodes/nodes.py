from typing import Dict, Any
from agents.IngestionAgent import IngestionAgent
from agents.NotemakingAgent import NotemakingAgent  
from agents.ConceptExtractionAgent import ConceptExtractionAgent
from agents.TagGenerator import TagGenerator
from agents.WebResourceFinderAgent import WebResourceFinderAgent
from agents.StyleRewriterAgent import StyleRewriterAgent
from state_schema import PipelineState


def ingestion_node(state: PipelineState) -> PipelineState:
    print("---INGESTION NODE---")
    print(state)
    agent = IngestionAgent(use_semantic=False)
    result = agent.run(state["input_source"])

    if result["status"] == "error":
        raise Exception(result["message"])

    new_state = {
        **state,
        "ingestion_status": result["status"],
        "ingested_source": result["source"],
        "documents": result["documents"],
        "ingestion_meta": result["meta"],
    }
    return new_state

def notemaking_node(state: PipelineState) -> PipelineState:
    print("---NOTEMAKING NODE---")
    user_instruction = state.get("user_instruction", None)
    agent = NotemakingAgent(api_key=state.get("api_key"))
    cleaned_docs = agent.run(state["documents"], user_instruction=user_instruction)

    new_state = {
        **state,
        "notemaking_status": "success",
        "clean_documents": cleaned_docs
    }
    return new_state

def concept_extraction_node(state: PipelineState) -> PipelineState:
    print("---CONCEPT EXTRACTION NODE---")
    agent = ConceptExtractionAgent()
    docs_with_concepts = agent.run(state["clean_documents"])

    concepts = []
    for doc in docs_with_concepts:
        concepts.extend(doc.metadata.get("concepts", []))

    new_state = {
        **state,
        "concept_extraction_status": "success",
        "documents_with_concepts": docs_with_concepts,
        "concepts": list(set(concepts))
    }
    return new_state

def tag_generator_node(state: PipelineState) -> PipelineState:
    print("---TAG GENERATOR NODE---")
    agent = TagGenerator()
    docs_with_tags = agent.run(state["documents_with_concepts"])

    all_tags = []
    for doc in docs_with_tags:
        all_tags.extend(doc.metadata.get("tags", []))

    new_state = {
        # **state,  // Not in parallel nodes it will OVERWRITE state keys
        "tag_generation_status": "success",
        "documents_with_tags": docs_with_tags, # Storing docs with tags in a new key
        "tags": list(set(all_tags)) # Extracting unique tags
    }
    return new_state

def websearch_node(state: PipelineState) -> PipelineState:
    print("---WEB SEARCH NODE---")
    agent = WebResourceFinderAgent()
    docs_with_resources = agent.run(state["documents_with_concepts"])

    all_resources = {}
    for doc in docs_with_resources:
        for concept, links in doc.metadata.get("resources", {}).items():
            if concept not in all_resources:
                all_resources[concept] = []
            all_resources[concept].extend(links)

    new_state = {
        # **state,  // Not in parallel nodes it will OVERWRITE state keys
        "web_search_status": "success",
        "documents_with_resources": docs_with_resources,
        "resources": all_resources
    }
    return new_state

def style_rewriter_node(state: PipelineState) -> PipelineState:
    print("---STYLE REWRITER NODE---")
    agent = StyleRewriterAgent(api_key=state.get("api_key"))

    concatenated_notes = "\n\n".join([doc.page_content for doc in state["clean_documents"]])
    result = agent.run(
        concatenated_notes,
        profile_path=state.get("profile_path"),
        profile_id=state.get("profile_id"),
        profile= state.get("style_profile")
    )

    new_state = {
        # **state,  // Not in parallel nodes it will OVERWRITE state keys
        "style_rewrite_status": "success",
        "rewritten_notes": result["rewritten_text"],
        "evaluation": result["evaluation"],
        "feedback": result["feedback"],
        "total_score": result["total_score"]
    }
    return new_state


## --- Style Learner ---


