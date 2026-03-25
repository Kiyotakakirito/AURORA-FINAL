"""
ProjectService using Supabase REST API (port 443 / HTTPS).
All methods mirror the old SQLAlchemy-based signatures so the router is untouched.
"""
from typing import List, Optional, Any
from types import SimpleNamespace
from ..core.supabase_client import get_supabase
from ..schemas import schemas

TABLE = "projects"
EVAL_TABLE = "evaluations"


def _row(data: dict) -> SimpleNamespace:
    """Convert a Supabase response row dict into an object with attribute access."""
    return SimpleNamespace(**data)


def _rows(data: list) -> List[SimpleNamespace]:
    return [_row(r) for r in (data or [])]


class ProjectService:
    # ─── Create ───────────────────────────────────────────────────────────────
    def create_project(
        self,
        db: Any,               # kept for signature compat — unused
        project: schemas.ProjectCreate,
        file_path: Optional[str] = None,
        pdf_path: Optional[str] = None,
    ) -> SimpleNamespace:
        sb = get_supabase()
        payload = {
            "name": project.name,
            "student_name": project.student_name,
            "student_email": project.student_email,
            "submission_type": project.submission_type,
            "github_url": project.github_url,
            "file_path": file_path,
            "pdf_path": pdf_path,
        }
        resp = sb.table(TABLE).insert(payload).execute()
        return _row(resp.data[0])

    # ─── Read ─────────────────────────────────────────────────────────────────
    def get_project(self, db: Any, project_id: int) -> Optional[SimpleNamespace]:
        sb = get_supabase()
        resp = sb.table(TABLE).select("*").eq("id", project_id).execute()
        rows = resp.data
        return _row(rows[0]) if rows else None

    def get_projects(
        self, db: Any, skip: int = 0, limit: int = 100
    ) -> List[SimpleNamespace]:
        sb = get_supabase()
        resp = (
            sb.table(TABLE)
            .select("*")
            .range(skip, skip + limit - 1)
            .order("id", desc=True)
            .execute()
        )
        return _rows(resp.data)

    def get_projects_by_student(
        self, db: Any, student_name: str, skip: int = 0, limit: int = 100
    ) -> List[SimpleNamespace]:
        sb = get_supabase()
        resp = (
            sb.table(TABLE)
            .select("*")
            .ilike("student_name", f"%{student_name}%")
            .range(skip, skip + limit - 1)
            .execute()
        )
        return _rows(resp.data)

    def search_projects(
        self, db: Any, query: str, skip: int = 0, limit: int = 100
    ) -> List[SimpleNamespace]:
        sb = get_supabase()
        # Use ilike filter; PostgREST doesn't support OR in a single call easily,
        # so we do two calls and merge (dedup by id).
        r1 = (
            sb.table(TABLE)
            .select("*")
            .ilike("name", f"%{query}%")
            .range(skip, skip + limit - 1)
            .execute()
        )
        r2 = (
            sb.table(TABLE)
            .select("*")
            .ilike("student_name", f"%{query}%")
            .range(skip, skip + limit - 1)
            .execute()
        )
        seen, combined = set(), []
        for row in (r1.data or []) + (r2.data or []):
            if row["id"] not in seen:
                seen.add(row["id"])
                combined.append(row)
        return _rows(combined[:limit])

    # ─── Update ───────────────────────────────────────────────────────────────
    def update_project(
        self, db: Any, project_id: int, project: schemas.ProjectUpdate
    ) -> Optional[SimpleNamespace]:
        sb = get_supabase()
        payload = project.dict(exclude_unset=True)
        if not payload:
            return self.get_project(db, project_id)
        resp = sb.table(TABLE).update(payload).eq("id", project_id).execute()
        rows = resp.data
        return _row(rows[0]) if rows else None

    # ─── Delete ───────────────────────────────────────────────────────────────
    def delete_project(self, db: Any, project_id: int) -> bool:
        sb = get_supabase()
        # Remove evaluations first
        sb.table(EVAL_TABLE).delete().eq("project_id", project_id).execute()
        resp = sb.table(TABLE).delete().eq("id", project_id).execute()
        return bool(resp.data)

    # ─── Aggregates ───────────────────────────────────────────────────────────
    def get_project_count(self, db: Any) -> int:
        sb = get_supabase()
        resp = sb.table(TABLE).select("id", count="exact").execute()
        return resp.count or 0

    def get_submission_type_counts(self, db: Any) -> dict:
        sb = get_supabase()
        resp = sb.table(TABLE).select("submission_type").execute()
        counts: dict = {}
        for row in (resp.data or []):
            t = row.get("submission_type")
            if t:
                counts[t] = counts.get(t, 0) + 1
        return counts
