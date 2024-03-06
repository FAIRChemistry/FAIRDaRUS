import sdRDM

from typing import Optional
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature


@forge_signature
class Keyword(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRDaRUS@1be591e1a58dc9e5896ef1736a250ce7f77923ef#Keyword"
    },
):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    value: Optional[str] = element(
        description="key terms describing important aspects of the dataset.",
        default=None,
        tag="value",
        json_schema_extra=dict(),
    )

    vocabulary: Optional[str] = element(
        description=(
            "for the specification of the keyword controlled vocabulary in use, such as"
            " LCSH, MeSH, or others."
        ),
        default=None,
        tag="vocabulary",
        json_schema_extra=dict(),
    )

    vocabulary_uri: Optional[str] = element(
        description=(
            "keyword vocabulary URI points to the web presence that describes the"
            " keyword vocabulary, if appropriate."
        ),
        default=None,
        tag="vocabulary_uri",
        json_schema_extra=dict(),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRDaRUS"
    )
    _commit: Optional[str] = PrivateAttr(
        default="1be591e1a58dc9e5896ef1736a250ce7f77923ef"
    )
