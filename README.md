# Bitespeed Identity API
The API is hosted on AWS on EC2 Instance, please find the Endpoint details below.

## Live Endpoint

Root: http://3.109.133.79:8000/

Identify: http://3.109.133.79:8000/identify

Request Body

```json
{
  "email": "nikit@gmail.com",
  "phoneNumber": "1234567890"
}
```
Response Body

```json
{
  "contact": {
    "primaryContatctId": 1,
    "emails": ["nikit@gmail.com"],
    "phoneNumbers": ["1234567890"],
    "secondaryContactIds": []
  }
}
```