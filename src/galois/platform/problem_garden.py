"""PostgreSQL-backed Problem Garden storage."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any
from uuid import uuid4

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb


GARDEN_PROBLEM_SEEDS: list[dict[str, Any]] = [
    {
        "id": "pfr-finite-fields",
        "title": "Polynomial Freiman-Ruzsa conjecture",
        "status": "open",
        "difficulty": "frontier",
        "domains": ["additive combinatorics", "finite fields"],
        "source": "S. Peluse, Finite field models in arithmetic combinatorics -- twenty years on, Surveys in Combinatorics 2024.",
        "source_url": "benchmarks/problems/finite_fields/polynomial Freiman-Ruzsa conjecture.md",
        "context": "This is the polynomial Freiman-Ruzsa conjecture in the finite-field model.",
        "statement": """Let $p$ be a fixed prime and let $A \\subseteq \\mathbb{F}_p^n$ satisfy
$$
|A+A| \\le K|A|.
$$
Must there exist a subspace $H \\le \\mathbb{F}_p^n$ with $|H| \\le |A|$ such that $A$ can be covered by at most $K^{O(1)}$ cosets of $H$?""",
        "source_literature": [
            "S. Peluse, Finite field models in arithmetic combinatorics -- twenty years on, Surveys in Combinatorics 2024.",
            "B. Green, Notes on the polynomial Freiman-Ruzsa conjecture, unpublished notes, 2005.",
        ],
        "attempted_literature": [
            "S. Lovett, Equivalence of polynomial conjectures in additive combinatorics, Combinatorica 32 (2012), 607-618.",
        ],
        "related_literature": [
            "Green-Tao style finite-field additive combinatorics surveys.",
            "Bogolyubov-Ruzsa type covering theorems over finite vector spaces.",
        ],
        "known_core_ideas": [
            "Small doubling should force low-complexity additive structure.",
            "Known routes compare covering, modeling, and inverse theorem formulations.",
            "Quantitative polynomial dependence on $K$ is the central obstruction.",
        ],
        "progress": [
            "Several polynomial conjectures are known to be equivalent in finite-field models.",
            "The benchmark formulation asks for better covering bounds or explicit structural extraction.",
        ],
        "possible_ideas": [
            "Track which equivalent formulation gives the most direct attack for a given $p$ and $K$.",
            "Compare recent finite-field survey reductions against older unpublished notes.",
        ],
        "graph_links": [
            {"from": "Problem", "relation": "stated_in", "to": "Peluse 2024 survey"},
            {"from": "Problem", "relation": "attempted_by", "to": "Lovett 2012"},
            {"from": "Problem", "relation": "uses_method", "to": "Bogolyubov-Ruzsa covering"},
            {"from": "Problem", "relation": "belongs_to_domain", "to": "Additive combinatorics"},
        ],
    },
    {
        "id": "primitive-completely-normal",
        "title": "Primitive completely normal elements",
        "status": "open",
        "difficulty": "research",
        "domains": ["finite fields", "field arithmetic"],
        "source": "Finite-field benchmark problem collection in Galois.",
        "source_url": "benchmarks/problems/finite_fields/primitive completely normal problem.md",
        "context": "This finite-field problem is useful for testing the boundary between algebraic existence results and explicit construction methods.",
        "statement": "Determine sharp existence results for elements of finite field extensions that are simultaneously primitive and completely normal over every intermediate subfield.",
        "source_literature": ["Finite-field normal basis and primitive element literature."],
        "attempted_literature": ["Character sum approaches to primitive normal basis problems."],
        "related_literature": [
            "Completely normal elements over finite fields.",
            "Primitive elements avoiding affine hyperplanes.",
        ],
        "known_core_ideas": [
            "Combine multiplicative primitivity with additive normality constraints.",
            "Character sums can separate some constraints but constants and small fields remain delicate.",
        ],
        "progress": [
            "Many extension-degree regimes are known; sharp uniform results remain a useful benchmark target.",
        ],
        "possible_ideas": [
            "Build a case table by extension degree and field size, then isolate the remaining exceptional regimes.",
        ],
        "graph_links": [
            {"from": "Problem", "relation": "related_to", "to": "Normal basis theorem"},
            {"from": "Problem", "relation": "uses_method", "to": "Character sums"},
            {"from": "Problem", "relation": "belongs_to_domain", "to": "Finite fields"},
        ],
    },
    {
        "id": "lehmer-mahler-measure",
        "title": "Lehmer's problem on Mahler measure",
        "status": "open",
        "difficulty": "frontier",
        "domains": ["number theory", "arithmetic dynamics"],
        "source": "Benchmark problem collection; classical formulation due to Lehmer.",
        "source_url": "benchmarks/problems/number_theory/Lehmer's problem on Mahler measure.md",
        "context": "This classical problem asks for a uniform gap in Mahler measure outside cyclotomic factors.",
        "statement": "Is there a universal constant $c>1$ such that every noncyclotomic monic integer polynomial has Mahler measure at least $c$?",
        "source_literature": [
            "D. H. Lehmer, Factorization of certain cyclotomic functions, Annals of Mathematics 34 (1933).",
        ],
        "attempted_literature": [
            "Dobrowolski-type lower bounds for Mahler measure.",
            "Surveys on Lehmer-type problems and heights.",
        ],
        "related_literature": [
            "Height lower bounds.",
            "Salem numbers and cyclotomic factors.",
        ],
        "known_core_ideas": [
            "Exclude cyclotomic factors and seek a uniform height gap.",
            "Known lower bounds depend on polynomial degree.",
        ],
        "progress": ["No degree-independent gap is known in the full classical form."],
        "possible_ideas": [
            "Compare special families where stronger lower bounds are known against the unrestricted problem.",
        ],
        "graph_links": [
            {"from": "Problem", "relation": "stated_in", "to": "Lehmer 1933"},
            {"from": "Problem", "relation": "related_to", "to": "Heights"},
            {"from": "Problem", "relation": "belongs_to_domain", "to": "Number theory"},
        ],
    },
]


PROBLEM_FIELDS = (
    "id",
    "title",
    "status",
    "difficulty",
    "domains",
    "source",
    "source_url",
    "context",
    "statement",
    "source_literature",
    "attempted_literature",
    "related_literature",
    "known_core_ideas",
    "progress",
    "possible_ideas",
)


class ProblemGardenStore:
    """Small repository wrapper for the Problem Garden PostgreSQL tables."""

    def __init__(self, database_url: str):
        self.database_url = database_url
        self._connection: psycopg.Connection[dict[str, Any]] | None = None

    def __enter__(self) -> "ProblemGardenStore":
        self._connection = psycopg.connect(self.database_url, row_factory=dict_row)
        return self

    def __exit__(self, *_exc: object) -> None:
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    @property
    def connection(self) -> psycopg.Connection[dict[str, Any]]:
        if self._connection is None:
            raise RuntimeError("ProblemGardenStore must be used as a context manager")
        return self._connection

    def initialize(self) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS garden_problems (
                    id text PRIMARY KEY,
                    title text NOT NULL,
                    statement text NOT NULL,
                    status text NOT NULL,
                    difficulty text NOT NULL,
                    domains text[] NOT NULL DEFAULT '{}',
                    source text NOT NULL DEFAULT '',
                    source_url text NOT NULL DEFAULT '',
                    context text NOT NULL DEFAULT '',
                    source_literature jsonb NOT NULL DEFAULT '[]'::jsonb,
                    attempted_literature jsonb NOT NULL DEFAULT '[]'::jsonb,
                    related_literature jsonb NOT NULL DEFAULT '[]'::jsonb,
                    known_core_ideas jsonb NOT NULL DEFAULT '[]'::jsonb,
                    progress jsonb NOT NULL DEFAULT '[]'::jsonb,
                    possible_ideas jsonb NOT NULL DEFAULT '[]'::jsonb,
                    created_at timestamptz NOT NULL DEFAULT now(),
                    updated_at timestamptz NOT NULL DEFAULT now()
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS garden_edges (
                    id bigserial PRIMARY KEY,
                    problem_id text NOT NULL REFERENCES garden_problems(id) ON DELETE CASCADE,
                    from_label text NOT NULL,
                    relation text NOT NULL,
                    to_label text NOT NULL,
                    created_at timestamptz NOT NULL DEFAULT now()
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS garden_submissions (
                    id text PRIMARY KEY,
                    title text NOT NULL,
                    statement text NOT NULL,
                    source_url text NOT NULL,
                    domain text NOT NULL DEFAULT '',
                    context text NOT NULL DEFAULT '',
                    references_text text NOT NULL DEFAULT '',
                    status text NOT NULL DEFAULT 'pending_review',
                    created_at timestamptz NOT NULL DEFAULT now()
                )
                """
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS garden_problems_status_idx ON garden_problems(status)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS garden_problems_difficulty_idx ON garden_problems(difficulty)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS garden_edges_problem_id_idx ON garden_edges(problem_id)"
            )
        self._seed_defaults()
        self.connection.commit()

    def _seed_defaults(self) -> None:
        with self.connection.cursor() as cursor:
            for problem in GARDEN_PROBLEM_SEEDS:
                values = {field: problem.get(field, [] if field.endswith("_literature") else "") for field in PROBLEM_FIELDS}
                cursor.execute(
                    """
                    INSERT INTO garden_problems (
                        id,
                        title,
                        status,
                        difficulty,
                        domains,
                        source,
                        source_url,
                        context,
                        statement,
                        source_literature,
                        attempted_literature,
                        related_literature,
                        known_core_ideas,
                        progress,
                        possible_ideas
                    )
                    VALUES (
                        %(id)s,
                        %(title)s,
                        %(status)s,
                        %(difficulty)s,
                        %(domains)s,
                        %(source)s,
                        %(source_url)s,
                        %(context)s,
                        %(statement)s,
                        %(source_literature)s::jsonb,
                        %(attempted_literature)s::jsonb,
                        %(related_literature)s::jsonb,
                        %(known_core_ideas)s::jsonb,
                        %(progress)s::jsonb,
                        %(possible_ideas)s::jsonb
                    )
                    ON CONFLICT (id) DO NOTHING
                    """,
                    {
                        **values,
                        "source_literature": Jsonb(values["source_literature"]),
                        "attempted_literature": Jsonb(values["attempted_literature"]),
                        "related_literature": Jsonb(values["related_literature"]),
                        "known_core_ideas": Jsonb(values["known_core_ideas"]),
                        "progress": Jsonb(values["progress"]),
                        "possible_ideas": Jsonb(values["possible_ideas"]),
                    },
                )
                cursor.execute("SELECT 1 FROM garden_edges WHERE problem_id = %s LIMIT 1", (problem["id"],))
                if cursor.fetchone():
                    continue
                cursor.executemany(
                    """
                    INSERT INTO garden_edges (problem_id, from_label, relation, to_label)
                    VALUES (%(problem_id)s, %(from)s, %(relation)s, %(to)s)
                    """,
                    [{**edge, "problem_id": problem["id"]} for edge in problem["graph_links"]],
                )

    def list_problems(
        self,
        *,
        query: str | None = None,
        status: str | None = None,
        domain: str | None = None,
        difficulty: str | None = None,
    ) -> list[dict[str, Any]]:
        clauses = []
        params: dict[str, Any] = {}
        if query:
            clauses.append("(title ILIKE %(query)s OR statement ILIKE %(query)s OR source ILIKE %(query)s)")
            params["query"] = f"%{query}%"
        if status:
            clauses.append("status = %(status)s")
            params["status"] = status
        if domain:
            clauses.append("%(domain)s = ANY(domains)")
            params["domain"] = domain
        if difficulty:
            clauses.append("difficulty = %(difficulty)s")
            params["difficulty"] = difficulty

        where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT
                    id,
                    title,
                    status,
                    difficulty,
                    domains,
                    source,
                    source_url,
                    context,
                    statement,
                    jsonb_array_length(related_literature) AS related_literature_count,
                    COALESCE(progress ->> 0, '') AS latest_progress
                FROM garden_problems
                {where_sql}
                ORDER BY
                    CASE difficulty
                        WHEN 'frontier' THEN 0
                        WHEN 'research' THEN 1
                        WHEN 'graduate' THEN 2
                        ELSE 3
                    END,
                    title
                LIMIT 200
                """,
                params,
            )
            return [dict(row) for row in cursor.fetchall()]

    def get_problem(self, problem_id: str) -> dict[str, Any] | None:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    title,
                    status,
                    difficulty,
                    domains,
                    source,
                    source_url,
                    context,
                    statement,
                    source_literature,
                    attempted_literature,
                    related_literature,
                    known_core_ideas,
                    progress,
                    possible_ideas
                FROM garden_problems
                WHERE id = %s
                """,
                (problem_id,),
            )
            problem = cursor.fetchone()
            if problem is None:
                return None
            cursor.execute(
                """
                SELECT from_label AS "from", relation, to_label AS "to"
                FROM garden_edges
                WHERE problem_id = %s
                ORDER BY id
                """,
                (problem_id,),
            )
            detail = dict(problem)
            detail["graph_links"] = [dict(row) for row in cursor.fetchall()]
            return detail

    def create_submission(self, payload: dict[str, str]) -> dict[str, str]:
        submission_id = payload.get("id") or str(uuid4())
        status = payload.get("status") or "pending_review"
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO garden_submissions (
                    id,
                    title,
                    statement,
                    source_url,
                    domain,
                    context,
                    references_text,
                    status
                )
                VALUES (
                    %(id)s,
                    %(title)s,
                    %(statement)s,
                    %(source_url)s,
                    %(domain)s,
                    %(context)s,
                    %(references_text)s,
                    %(status)s
                )
                """,
                {
                    **payload,
                    "id": submission_id,
                    "status": status,
                    "domain": payload.get("domain", ""),
                    "context": payload.get("context", ""),
                    "references_text": payload.get("references_text", ""),
                },
            )
        self.connection.commit()
        return {"submission_id": submission_id, "status": status}


def normalize_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    if isinstance(value, Iterable) and not isinstance(value, str):
        return list(value)
    return [value]
