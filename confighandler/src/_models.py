""" Pydantic models used in the module """

from pydantic import BaseModel, ConfigDict, computed_field
from ._constants import TYPE_DEFINITIONS, TYPE_MAPPERS


class Row(BaseModel):
    """
    Model for a database row with automatic type conversion
    """

    model_config = ConfigDict(
        extra="allow",
        arbitrary_types_allowed=True  # Allow DictRow and dict types
    )

    row:dict

    @computed_field
    @property
    def name(self) -> str:
        """
        Returns the "name" of attribute.
        """
        return self.row["name"]

    @computed_field
    @property
    def value_type(self) -> type:
        """
        Returns the value type of the object retrieved
        """
        return TYPE_DEFINITIONS.get(self.row["type_id"], type(None))

    @computed_field
    @property
    def value(
        self,
    ) -> str | int | float | bool | list[str] | list[int] | list[float] | None:
        """
        Map type_id to the appropriate type and extract the value.

        Args:
            type_id: The type identifier from the database
            raw_value: The raw string value from the database

        Returns:
            The converted value with the appropriate type
        """

        mapper = TYPE_MAPPERS.get(self.row["type_id"])
        if mapper is None:
            raise ValueError("Incompatibile type is given")

        try:
            return mapper(self.row["value"])
        except (ValueError, TypeError) as e:
            raise ValueError(
                f"Failed to convert value '{self.row['value']}' with type_id {self.row['type_id']}: {e}"
            ) from e
