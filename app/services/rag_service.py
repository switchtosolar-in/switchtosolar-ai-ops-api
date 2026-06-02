"""
RAG and AI Ops orchestration service.

This file coordinates the main AI Ops question-answering workflow:

User/Admin question
  -> request ID creation
  -> intent/tool classification
  -> unsupported response OR operational retrieval OR RAG retrieval
  -> prompt construction
  -> LLM execution
  -> source/metadata formatting
  -> query logging

This service acts as the workflow coordinator. Lower-level retrieval,
prompt building, LLM calls, operational data access, and logging are
delegated to dedicated services and repositories.
"""

from app.repositories.query_log_repository import insert_query_log
from app.services.tool_router import classify_tool
from app.services.retrieval_service import retrieve_relevant_chunks
from app.services.prompt_builder import build_prompt
from app.services.ops_service import answer_operations_question
from app.services.llm_service import generate_answer
from app.utils.ids import create_request_id
from app.utils.timing import now_ms, elapsed_ms


def answer_question(question: str, top_k: int = 3) -> dict:
    request_id = create_request_id()
    start_ms = now_ms()

    route_decision = classify_tool(question)
    intent = route_decision["intent"]

    try:
        if intent == "unsupported":
            answer = (
                "I can only answer questions related to SwitchToSolar knowledge "
                "or platform operations."
            )
            latency_ms = elapsed_ms(start_ms)

            insert_query_log(
                request_id=request_id,
                question=question,
                answer=answer,
                intent_type=intent,
                retrieved_chunk_ids=[],
                similarity_scores=[],
                model_used="none",
                latency_ms=latency_ms,
                status="success",
            )

            return {
                "question": question,
                "answer": answer,
                "intent": intent,
                "sources": [],
                "metadata": {
                    "request_id": request_id,
                    "model": "none",
                    "chunks_used": 0,
                    "latency_ms": latency_ms,
                    "retrieval_confidence": None,
                    "best_distance": None,
                },
            }

        if intent == "operations":
            ops_response = answer_operations_question(question, route_decision)
            latency_ms = elapsed_ms(start_ms)

            insert_query_log(
                request_id=request_id,
                question=question,
                answer=ops_response["answer"],
                intent_type=intent,
                retrieved_chunk_ids=[],
                similarity_scores=[],
                model_used="none",
                latency_ms=latency_ms,
                status="success",
                data_source="mssql",
                operation_tool=ops_response["tool"],
                operation_data=ops_response["data"],
            )

            return {
                "question": question,
                "answer": ops_response["answer"],
                "intent": intent,
                "sources": [],
                "metadata": {
                    "request_id": request_id,
                    "model": "none",
                    "chunks_used": 0,
                    "latency_ms": latency_ms,
                    "retrieval_confidence": None,
                    "best_distance": None,
                    "data_source": "mssql",
                    "operation_tool": ops_response["tool"],
                    "operation_data": ops_response["data"],
                },
            }

        retrieval_result = retrieve_relevant_chunks(
            question=question,
            top_k=top_k,
        )

        chunks = retrieval_result["chunks"]
        retrieval_confidence = retrieval_result["confidence"]
        best_distance = retrieval_result["best_distance"]

        if not chunks:
            answer = (
                "I don't have enough relevant information in the SwitchToSolar knowledge base "
                "to answer this confidently."
            )
            latency_ms = elapsed_ms(start_ms)

            insert_query_log(
                request_id=request_id,
                question=question,
                answer=answer,
                intent_type=intent,
                retrieved_chunk_ids=[],
                similarity_scores=[],
                model_used="none",
                latency_ms=latency_ms,
                status="success",
            )

            return {
                "question": question,
                "answer": answer,
                "intent": intent,
                "sources": [],
                "metadata": {
                    "request_id": request_id,
                    "model": "none",
                    "chunks_used": 0,
                    "latency_ms": latency_ms,
                    "retrieval_confidence": retrieval_confidence,
                    "best_distance": best_distance,
                },
            }

        prompt = build_prompt(
            question=question,
            chunks=chunks,
        )

        llm_response = generate_answer(
            system_prompt=prompt["system"],
            user_prompt=prompt["user"],
        )

        sources = [
            {
                "document_title": chunk["document_title"],
                "chunk_index": chunk["chunk_index"],
                "distance": chunk["distance"],
            }
            for chunk in chunks
        ]

        latency_ms = elapsed_ms(start_ms)

        insert_query_log(
            request_id=request_id,
            question=question,
            answer=llm_response["answer"],
            intent_type=intent,
            retrieved_chunk_ids=[chunk["chunk_id"] for chunk in chunks],
            similarity_scores=[chunk["distance"] for chunk in chunks],
            model_used=llm_response["model"],
            latency_ms=latency_ms,
            status="success",
        )

        return {
            "question": question,
            "answer": llm_response["answer"],
            "intent": intent,
            "sources": sources,
            "metadata": {
                "request_id": request_id,
                "model": llm_response["model"],
                "chunks_used": len(chunks),
                "latency_ms": latency_ms,
                "retrieval_confidence": retrieval_confidence,
                "best_distance": best_distance,
            },
        }

    except Exception as error:
        latency_ms = elapsed_ms(start_ms)
        error_message = str(error)

        insert_query_log(
            request_id=request_id,
            question=question,
            answer="",
            intent_type=intent,
            retrieved_chunk_ids=[],
            similarity_scores=[],
            model_used="unknown",
            latency_ms=latency_ms,
            status="error",
            error_message=error_message,
        )

        raise