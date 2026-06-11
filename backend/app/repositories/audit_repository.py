from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


class AuditRepository:
    def create(
        self,
        db: Session,
        event_type: str,
        entity: str,
        entity_id: str | None,
    ) -> AuditLog:
        audit_log = AuditLog(
            event_type=event_type,
            entity=entity,
            entity_id=entity_id,
        )
        db.add(audit_log)
        return audit_log
