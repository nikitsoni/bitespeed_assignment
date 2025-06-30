from pydantic import BaseModel
from typing import Optional, List

class IdentifyRequest(BaseModel):
    email: Optional[str] = None
    phoneNumber: Optional[str] = None

class ContactResponse(BaseModel):
    primaryContactId: int
    emails: List[str]
    phoneNumbers: List[str]
    secondaryContactIds: List[str]

class IdentifyResponse(BaseModel):
    contact: ContactResponse