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
        "source_url": "https://doi.org/10.1017/9781009567174.011",
        "statement": """Let $p$ be a fixed prime and let $A \\subseteq \\mathbb{F}_p^n$ satisfy
$$
|A+A| \\le K|A|.
$$
Must there exist a subspace $H \\le \\mathbb{F}_p^n$ with $|H| \\le |A|$ such that $A$ can be covered by at most $K^{O(1)}$ cosets of $H$?""",
        "source_literature": [
            "S. Peluse, Finite field models in arithmetic combinatorics -- twenty years on, Surveys in Combinatorics 2024.",
            "B. Green, Notes on the polynomial Freiman-Ruzsa conjecture, unpublished notes, 2005.",
        ],
        "progress": [
            "Several polynomial conjectures are known to be equivalent in finite-field models.",
            "The benchmark formulation asks for better covering bounds or explicit structural extraction.",
        ],
        "community_reactions": [],
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
        "source": "S. D. Cohen and S. Huczynska, The primitive normal basis theorem -- without a computer, Journal of Pure and Applied Algebra 223 (2019).",
        "source_url": "https://doi.org/10.1016/j.jpaa.2018.09.003",
        "statement": "Determine sharp existence results for elements of finite field extensions that are simultaneously primitive and completely normal over every intermediate subfield.",
        "source_literature": ["Finite-field normal basis and primitive element literature."],
        "progress": [
            "Many extension-degree regimes are known; sharp uniform results remain a useful benchmark target.",
        ],
        "community_reactions": [],
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
        "source": "D. H. Lehmer, Factorization of certain cyclotomic functions, Annals of Mathematics 34 (1933).",
        "source_url": "https://doi.org/10.2307/1968393",
        "statement": "Is there a universal constant $c>1$ such that every noncyclotomic monic integer polynomial has Mahler measure at least $c$?",
        "source_literature": [
            "D. H. Lehmer, Factorization of certain cyclotomic functions, Annals of Mathematics 34 (1933).",
        ],
        "progress": ["No degree-independent gap is known in the full classical form."],
        "community_reactions": [],
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
    "statement",
    "source_literature",
    "progress",
    "community_reactions",
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
                    source_literature jsonb NOT NULL DEFAULT '[]'::jsonb,
                    progress jsonb NOT NULL DEFAULT '[]'::jsonb,
                    community_reactions jsonb NOT NULL DEFAULT '[]'::jsonb,
                    created_at timestamptz NOT NULL DEFAULT now(),
                    updated_at timestamptz NOT NULL DEFAULT now()
                )
                """
            )
            cursor.execute(
                "ALTER TABLE garden_problems ADD COLUMN IF NOT EXISTS community_reactions jsonb NOT NULL DEFAULT '[]'::jsonb"
            )
            cursor.execute("ALTER TABLE garden_problems DROP COLUMN IF EXISTS context")
            cursor.execute("ALTER TABLE garden_problems DROP COLUMN IF EXISTS related_literature")
            cursor.execute("ALTER TABLE garden_problems DROP COLUMN IF EXISTS attempted_literature")
            cursor.execute("ALTER TABLE garden_problems DROP COLUMN IF EXISTS known_core_ideas")
            cursor.execute("ALTER TABLE garden_problems DROP COLUMN IF EXISTS possible_ideas")
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
                    source_literature jsonb NOT NULL DEFAULT '[]'::jsonb,
                    progress jsonb NOT NULL DEFAULT '[]'::jsonb,
                    status text NOT NULL DEFAULT 'pending_review',
                    created_at timestamptz NOT NULL DEFAULT now()
                )
                """
            )
            cursor.execute("ALTER TABLE garden_submissions DROP COLUMN IF EXISTS context")
            cursor.execute("ALTER TABLE garden_submissions DROP COLUMN IF EXISTS references_text")
            cursor.execute(
                "ALTER TABLE garden_submissions ADD COLUMN IF NOT EXISTS source_literature jsonb NOT NULL DEFAULT '[]'::jsonb"
            )
            cursor.execute(
                "ALTER TABLE garden_submissions ADD COLUMN IF NOT EXISTS progress jsonb NOT NULL DEFAULT '[]'::jsonb"
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS garden_import_batches (
                    id text PRIMARY KEY,
                    source_name text NOT NULL,
                    source_url text NOT NULL,
                    item_count integer NOT NULL,
                    imported_count integer NOT NULL,
                    skipped_count integer NOT NULL,
                    fetch_pages boolean NOT NULL DEFAULT false,
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
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS garden_problems_source_url_idx ON garden_problems(source_url)"
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
                        statement,
                        source_literature,
                        progress,
                        community_reactions
                    )
                    VALUES (
                        %(id)s,
                        %(title)s,
                        %(status)s,
                        %(difficulty)s,
                        %(domains)s,
                        %(source)s,
                        %(source_url)s,
                        %(statement)s,
                        %(source_literature)s::jsonb,
                        %(progress)s::jsonb,
                        %(community_reactions)s::jsonb
                    )
                    ON CONFLICT (id) DO UPDATE SET
                        title = EXCLUDED.title,
                        statement = EXCLUDED.statement,
                        status = EXCLUDED.status,
                        difficulty = EXCLUDED.difficulty,
                        domains = EXCLUDED.domains,
                        source = EXCLUDED.source,
                        source_url = EXCLUDED.source_url,
                        source_literature = EXCLUDED.source_literature,
                        progress = EXCLUDED.progress,
                        community_reactions = EXCLUDED.community_reactions,
                        updated_at = now()
                    """,
                    {
                        **values,
                        "source_literature": Jsonb(values["source_literature"]),
                        "progress": Jsonb(values["progress"]),
                        "community_reactions": Jsonb(values["community_reactions"]),
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

    def upsert_problem(self, problem: dict[str, Any]) -> str:
        values = {field: problem.get(field, [] if field.endswith("_literature") else "") for field in PROBLEM_FIELDS}
        with self.connection.cursor() as cursor:
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
                    statement,
                    source_literature,
                    progress,
                    community_reactions
                )
                VALUES (
                    %(id)s,
                    %(title)s,
                    %(status)s,
                    %(difficulty)s,
                    %(domains)s,
                    %(source)s,
                    %(source_url)s,
                    %(statement)s,
                    %(source_literature)s::jsonb,
                    %(progress)s::jsonb,
                    %(community_reactions)s::jsonb
                )
                ON CONFLICT (id) DO UPDATE SET
                    title = EXCLUDED.title,
                    statement = CASE
                        WHEN EXCLUDED.statement LIKE 'Metadata-only entry for Erdős problem #%%'
                             AND garden_problems.statement NOT LIKE 'Metadata-only entry for Erdős problem #%%'
                        THEN garden_problems.statement
                        ELSE EXCLUDED.statement
                    END,
                    status = EXCLUDED.status,
                    difficulty = EXCLUDED.difficulty,
                    domains = EXCLUDED.domains,
                    source = EXCLUDED.source,
                    source_url = EXCLUDED.source_url,
                    source_literature = EXCLUDED.source_literature,
                    progress = EXCLUDED.progress,
                    community_reactions = EXCLUDED.community_reactions,
                    updated_at = now()
                """,
                {
                    **values,
                    "source_literature": Jsonb(normalize_list(values["source_literature"])),
                    "progress": Jsonb(normalize_list(values["progress"])),
                    "community_reactions": Jsonb(normalize_list(values["community_reactions"])),
                },
            )
            cursor.execute("DELETE FROM garden_edges WHERE problem_id = %s", (values["id"],))
            graph_links = normalize_list(problem.get("graph_links"))
            if graph_links:
                cursor.executemany(
                    """
                    INSERT INTO garden_edges (problem_id, from_label, relation, to_label)
                    VALUES (%(problem_id)s, %(from)s, %(relation)s, %(to)s)
                    """,
                    [
                        {
                            "problem_id": values["id"],
                            "from": str(edge.get("from", "Problem")),
                            "relation": str(edge.get("relation", "related_to")),
                            "to": str(edge.get("to", "")),
                        }
                        for edge in graph_links
                        if str(edge.get("to", "")).strip()
                    ],
                )
        return values["id"]

    def upsert_problems(self, problems: Iterable[dict[str, Any]]) -> int:
        count = 0
        for problem in problems:
            self.upsert_problem(problem)
            count += 1
        self.connection.commit()
        return count

    def record_import_batch(
        self,
        *,
        batch_id: str,
        source_name: str,
        source_url: str,
        item_count: int,
        imported_count: int,
        skipped_count: int,
        fetch_pages: bool,
    ) -> None:
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO garden_import_batches (
                    id,
                    source_name,
                    source_url,
                    item_count,
                    imported_count,
                    skipped_count,
                    fetch_pages
                )
                VALUES (%(id)s, %(source_name)s, %(source_url)s, %(item_count)s, %(imported_count)s, %(skipped_count)s, %(fetch_pages)s)
                ON CONFLICT (id) DO UPDATE SET
                    source_name = EXCLUDED.source_name,
                    source_url = EXCLUDED.source_url,
                    item_count = EXCLUDED.item_count,
                    imported_count = EXCLUDED.imported_count,
                    skipped_count = EXCLUDED.skipped_count,
                    fetch_pages = EXCLUDED.fetch_pages
                """,
                {
                    "id": batch_id,
                    "source_name": source_name,
                    "source_url": source_url,
                    "item_count": item_count,
                    "imported_count": imported_count,
                    "skipped_count": skipped_count,
                    "fetch_pages": fetch_pages,
                },
            )
        self.connection.commit()

    def list_problems(
        self,
        *,
        query: str | None = None,
        status: str | None = None,
        domain: str | None = None,
        difficulty: str | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        clauses = []
        params: dict[str, Any] = {}
        params["limit"] = max(1, min(limit, 200))
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
        has_filters = bool(clauses)
        order_sql = (
            """
                    CASE difficulty
                        WHEN 'frontier' THEN 0
                        WHEN 'research' THEN 1
                        WHEN 'graduate' THEN 2
                        ELSE 3
                    END,
                    title
            """
            if has_filters
            else "random()"
        )
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
                    statement,
                    COALESCE(progress ->> 0, '') AS latest_progress
                FROM garden_problems
                {where_sql}
                ORDER BY {order_sql}
                LIMIT %(limit)s
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
                    statement,
                    source_literature,
                    progress,
                    community_reactions
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
                    source_literature,
                    progress,
                    status
                )
                VALUES (
                    %(id)s,
                    %(title)s,
                    %(statement)s,
                    %(source_url)s,
                    %(domain)s,
                    %(source_literature)s::jsonb,
                    %(progress)s::jsonb,
                    %(status)s
                )
                """,
                {
                    **payload,
                    "id": submission_id,
                    "status": status,
                    "domain": payload.get("domain", ""),
                    "source_literature": Jsonb(normalize_list(payload.get("source_literature"))),
                    "progress": Jsonb(normalize_list(payload.get("progress"))),
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
