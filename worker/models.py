from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class PrimaryData(BaseModel):
    id: UUID
    created_at: datetime
    last_update: datetime
    notification_id: UUID
    last_notification_send: Optional[datetime] = None
    source: str
    event_type: str
    content_id: UUID
    action: str
    data_endpoint: str
    in_queue: bool
