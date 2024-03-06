import sdRDM

from typing import Optional
from pydantic import PrivateAttr
from uuid import uuid4
from pydantic_xml import attr, element
from sdRDM.base.utils import forge_signature


@forge_signature
class TopicClassification(
    sdRDM.DataModel,
    nsmap={
        "": "https://github.com/FAIRChemistry/FAIRDaRUS@e1a9204c8b78f122dc20b27eb93861caec68a324#TopicClassification"
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
        description="topic or Subject term that is relevant to this Dataset.",
        default=None,
        tag="value",
        json_schema_extra=dict(),
    )

    vocab: Optional[str] = element(
        description=(
            "provided for specification of the controlled vocabulary in use, e.g.,"
            " LCSH, MeSH, etc."
        ),
        default=None,
        tag="vocab",
        json_schema_extra=dict(),
    )

    vocab_uri: Optional[str] = element(
        description="specifies the URI location for the full controlled vocabulary.",
        default=None,
        tag="vocab_uri",
        json_schema_extra=dict(),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRDaRUS"
    )
    _commit: Optional[str] = PrivateAttr(
        default="e1a9204c8b78f122dc20b27eb93861caec68a324"
    )
