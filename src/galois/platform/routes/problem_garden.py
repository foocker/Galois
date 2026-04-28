"""Problem Garden API routes."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from ..config import PlatformConfig
from ..problem_garden import ProblemGardenStore


class ProblemGardenSubmissionRequest(BaseModel):
    title: str = Field(min_length=1)
    statement: str = Field(min_length=1)
    source_url: str = Field(min_length=1)
    domain: str = ""
    source_literature: list[str] = Field(default_factory=list)
    progress: list[str] = Field(default_factory=list)


def garden_store_payload(payload: ProblemGardenSubmissionRequest) -> dict[str, str]:
    return {
        "title": payload.title.strip(),
        "statement": payload.statement.strip(),
        "source_url": payload.source_url.strip(),
        "domain": payload.domain.strip(),
        "source_literature": [item.strip() for item in payload.source_literature if item.strip()],
        "progress": [item.strip() for item in payload.progress if item.strip()],
        "status": "pending_review",
    }


def create_problem_garden_router(
    config: PlatformConfig,
    *,
    store_class: type[ProblemGardenStore] = ProblemGardenStore,
) -> APIRouter:
    router = APIRouter(prefix="/api/problem-garden", tags=["problem-garden"])

    @router.get("/problems")
    def list_problem_garden_problems(
        q: str | None = None,
        status: str | None = None,
        domain: str | None = None,
        difficulty: str | None = None,
    ) -> dict[str, Any]:
        with store_class(config.database.connection_url) as store:
            store.initialize()
            return {
                "problems": store.list_problems(
                    query=q.strip() if q else None,
                    status=status.strip() if status else None,
                    domain=domain.strip() if domain else None,
                    difficulty=difficulty.strip() if difficulty else None,
                )
            }

    @router.get("/problems/{problem_id}")
    def get_problem_garden_problem(problem_id: str) -> dict[str, Any]:
        with store_class(config.database.connection_url) as store:
            store.initialize()
            problem = store.get_problem(problem_id)
        if problem is None:
            raise HTTPException(status_code=404, detail="problem not found")
        return {"problem": problem}

    @router.post("/submissions")
    def create_problem_garden_submission(payload: ProblemGardenSubmissionRequest) -> JSONResponse:
        cleaned = garden_store_payload(payload)
        if not cleaned["title"]:
            raise HTTPException(status_code=400, detail="title must not be blank")
        if not cleaned["statement"]:
            raise HTTPException(status_code=400, detail="statement must not be blank")
        if not cleaned["source_url"]:
            raise HTTPException(status_code=400, detail="source_url must not be blank")
        with store_class(config.database.connection_url) as store:
            store.initialize()
            created = store.create_submission(cleaned)
        return JSONResponse(status_code=202, content=created)

    return router
