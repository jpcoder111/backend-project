from pydantic import BaseModel
from typing import Optional

class Customer(BaseModel):
    lastName: Optional[str] = None
    firstName: Optional[str] = None
    age: Optional[int] = None
    id: Optional[int] = None