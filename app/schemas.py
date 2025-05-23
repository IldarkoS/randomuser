from uuid import UUID

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: UUID
    gender: str
    first_name: str
    last_name: str
    phone: str
    email: str
    location: str
    photo_url: str

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
