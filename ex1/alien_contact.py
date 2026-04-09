from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from enum import Enum
from typing import Optional


class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(None, max_length=500)
    is_verified: bool = False

    @model_validator(mode='after')
    def validate_business_rules(self) -> 'AlienContact':
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")

        if self.contact_type == ContactType.physical and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")

        # telepathic contact requires at least 3 witnesses
        if (self.contact_type == ContactType.telepathic
                and self.witness_count < 3):
            raise ValueError("Telepathic contact requires at least 3 witnesses")

        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                "Strong signals (> 7.0) should include received messages")

        return self


def main():
    print("Alien Contact Log Validation")
    print("=" * 38)
    try:
        valid = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.now(),
            location="Area 51, Nevada",
            contact_type=ContactType.radio,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli"
        )
        print("Valid contact report:")
        print(f"ID: {valid.contact_id}")
        print(f"Type: {valid.contact_type.value}")
        print(f"Location: {valid.location}")
        print(f"Signal: {valid.signal_strength}/10")
        print(f"Duration: {valid.duration_minutes} minutes")
        print(f"Witnesses: {valid.witness_count}")
        print(f"Message: '{valid.message_received}'")
    except ValidationError as e:
        print(e.errors()[0]['msg'])
    except Exception as e:
        print(e)

    print()
    print("=" * 38)
    print("Expected validation error:")
    try:
        AlienContact(
            contact_id="AC_BAD",
            timestamp=datetime.now(),
            location="Unknown",
            contact_type=ContactType.telepathic,
            signal_strength=5.0,
            duration_minutes=10,
            witness_count=1
        )
    except ValidationError as e:
        print(e.errors()[0]['msg'])
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
