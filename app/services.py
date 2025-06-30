from sqlalchemy.orm import Session
from app import models
from app.schemas import IdentifyRequest, IdentifyResponse, ContactResponse
from sqlalchemy import or_

def identify_user(data: IdentifyRequest, db: Session) -> IdentifyResponse:
    
    email = data.email
    phone = data.phoneNumber
    
    existing_contacts = db.query(models.Contact).filter(
        or_(
            models.Contact.email == email,
            models.Contact.phone_number == phone
        )
    ).all()

    if not existing_contacts:
        
        new_contact = models.Contact(
            email=email,
            phone_number=phone,
            link_precedence='primary'
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        
        return IdentifyResponse(
            contact=ContactResponse(
                primaryContactId=new_contact.id,
                emails=[email] if email else [],
                phoneNumbers=[phone] if phone else [],
                secondaryContactIds=[]
            )
        )