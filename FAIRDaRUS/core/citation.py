import sdRDM

from typing import Dict, List, Optional
from pydantic import PrivateAttr, model_validator
from uuid import uuid4
from pydantic_xml import attr, element
from lxml.etree import _Element
from sdRDM.base.listplus import ListPlus
from sdRDM.base.utils import forge_signature
from sdRDM.tools.utils import elem2dict
from .author import Author


@forge_signature
class Contact(sdRDM.DataModel, search_mode="unordered"):
    """Small type for attribute 'contact'"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )
    name: Optional[str] = element(default=None, tag="name", json_schema_extra=dict())
    affiliation: Optional[str] = element(
        default=None, tag="affiliation", json_schema_extra=dict()
    )
    email: Optional[str] = element(default=None, tag="email", json_schema_extra=dict())
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRDaRUS"
    )
    _commit: Optional[str] = PrivateAttr(
        default="40b769959ec876653e2a7eab19d64d83f8ae9dd2"
    )
    _raw_xml_data: Dict = PrivateAttr(default_factory=dict)

    @model_validator(mode="after")
    def _parse_raw_xml_data(self):
        for attr, value in self:
            if isinstance(value, (ListPlus, list)) and all(
                (isinstance(i, _Element) for i in value)
            ):
                self._raw_xml_data[attr] = [elem2dict(i) for i in value]
            elif isinstance(value, _Element):
                self._raw_xml_data[attr] = elem2dict(value)
        return self


@forge_signature
class Citation(sdRDM.DataModel, search_mode="unordered"):
    """"""

    id: Optional[str] = attr(
        name="id",
        description="Unique identifier of the given object.",
        default_factory=lambda: str(uuid4()),
        xml="@id",
    )

    title: Optional[str] = element(
        description="title of the work.",
        default=None,
        tag="title",
        json_schema_extra=dict(),
    )

    project: Optional[str] = element(
        description="name of the project this work is related to.",
        default=None,
        tag="project",
        json_schema_extra=dict(),
    )

    description: Optional[str] = element(
        description="describtion of the content of the dataset.",
        default=None,
        tag="description",
        json_schema_extra=dict(),
    )

    authors: List[Author] = element(
        description="authors of this dataset.",
        default_factory=ListPlus,
        tag="authors",
        json_schema_extra=dict(multiple=True),
    )

    contact: Optional[Contact] = element(
        description="point of contact for this project.",
        default_factory=Contact,
        tag="contact",
        json_schema_extra=dict(),
    )

    subject: List[str] = element(
        description=(
            "domain specific subject categories that are topically relevant to the"
            " dataset."
        ),
        default_factory=ListPlus,
        tag="subject",
        json_schema_extra=dict(multiple=True),
    )
    _repo: Optional[str] = PrivateAttr(
        default="https://github.com/FAIRChemistry/FAIRDaRUS"
    )
    _commit: Optional[str] = PrivateAttr(
        default="40b769959ec876653e2a7eab19d64d83f8ae9dd2"
    )
    _raw_xml_data: Dict = PrivateAttr(default_factory=dict)

    @model_validator(mode="after")
    def _parse_raw_xml_data(self):
        for attr, value in self:
            if isinstance(value, (ListPlus, list)) and all(
                (isinstance(i, _Element) for i in value)
            ):
                self._raw_xml_data[attr] = [elem2dict(i) for i in value]
            elif isinstance(value, _Element):
                self._raw_xml_data[attr] = elem2dict(value)
        return self

    def add_to_authors(
        self,
        name: Optional[str] = None,
        affiliation: Optional[str] = None,
        id: Optional[str] = None,
        **kwargs
    ) -> Author:
        """
        This method adds an object of type 'Author' to attribute authors

        Args:
            id (str): Unique identifier of the 'Author' object. Defaults to 'None'.
            name (): full name including given and family name.. Defaults to None
            affiliation (): organization the author is affiliated to.. Defaults to None
        """
        params = {"name": name, "affiliation": affiliation}
        if id is not None:
            params["id"] = id
        self.authors.append(Author(**params))
        return self.authors[-1]
