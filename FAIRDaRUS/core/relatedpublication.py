import sdRDM

from typing import Optional
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature


@forge_signature
class RelatedPublication(
    sdRDM.DataModel,
):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    citation: Optional[str] = element(
        description="full bibliographic citation for this related publication.",
        default=None,
        tag="citation",
        json_schema_extra=dict(),
    )

    id_type: Optional[str] = element(
        description=(
            "type of digital identifier used for this publication, e.g., digital object"
            " identifier (DOI)."
        ),
        default=None,
        tag="id_type",
        json_schema_extra=dict(),
    )

    id_number: Optional[str] = element(
        description="identifier for the selected ID type.",
        default=None,
        tag="id_number",
        json_schema_extra=dict(),
    )

    url: Optional[str] = element(
        description=(
            "link to the publication web page, e.g., journal article page, archive"
            " record page, or other."
        ),
        default=None,
        tag="url",
        json_schema_extra=dict(),
    )