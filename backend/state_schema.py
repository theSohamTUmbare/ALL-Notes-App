from typing import List, Dict, Any, TypedDict, Optional, Union
from langgraph.graph import StateGraph, END, START
from langchain_core.documents import Document
from langchain_core.runnables import RunnableParallel

class PipelineState(TypedDict):
    ingestion_status: Optional[str]
    input_source: Optional[Union[str, List[str]]]
    documents: Optional[List[Document]]
    ingestion_meta: Optional[Dict[str, Any]]
    notemaking_status: Optional[str]
    clean_documents: Optional[List[Document]]
    concept_extraction_status: Optional[str]
    documents_with_concepts: Optional[List[Document]]
    concepts: Optional[List[str]]
    tag_generation_status: Optional[str]
    documents_with_tags: Optional[List[Document]]
    tags: Optional[List[str]]
    web_search_status: Optional[str]
    documents_with_resources: Optional[List[Document]]
    resources: Optional[Dict[str, Any]]
    style_rewrite_status: Optional[str]
    rewritten_notes: Optional[str]
    evaluation: Optional[Dict[str, Any]]
    feedback: Optional[str]
    total_score: Optional[float]
    user_choice: Optional[str]
    llm: Any
    retriever: Optional[Any]
    index_data: Optional[Dict[str, Any]]
    indexing_status: Optional[str]
    user_query: Optional[str]
    qna_output: Optional[Dict[str, Any]]
    user_interest: Optional[str]
    recommendations: Optional[str]
    llm: Optional[Any]
    api_key: Optional[str]
    profile_id: Optional[str]
    profile_path: Optional[str]
