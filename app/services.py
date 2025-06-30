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
    
    primary_contacts = [c for c in existing_contacts if c.link_precedence == "primary"]
    primary = min(primary_contacts, key=lambda c: c.created_at)
    
    emails = set(c.email for c in existing_contacts if c.email)
    phones = set(c.phone_number for c in existing_contacts if c.phone_number)

    new_data = (email and email not in emails) or (phone and phone not in phones)

    if new_data:
        new_secondary = models.Contact(
            email=email,
            phone_number=phone,
            link_precedence="secondary",
            linked_id=primary.id
        )
        db.add(new_secondary)
        db.commit()
        db.refresh(new_secondary)
        existing_contacts.append(new_secondary)
    
    contact_ids = [c.id for c in existing_contacts]
    linked_ids = [c.linked_id for c in existing_contacts if c.linked_id]
    all_ids = list(set(contact_ids + linked_ids))

    full_contacts = db.query(models.Contact).filter(
        or_(
            models.Contact.id.in_(all_ids),
            models.Contact.linked_id.in_(all_ids)
        )
    ).all()
    
    all_emails = list({c.email for c in full_contacts if c.email})
    all_phones = list({c.phone_number for c in full_contacts if c.phone_number})
    secondary_ids = [c.id for c in full_contacts if c.link_precedence == "secondary"]

    return IdentifyResponse(
        contact=ContactResponse(
            primaryContactId=primary.id,
            emails=[primary.email] + [e for e in all_emails if e != primary.email],
            phoneNumbers=[primary.phone_number] + [p for p in all_phones if p != primary.phone_number],
            secondaryContactIds=secondary_ids
        )
    )
