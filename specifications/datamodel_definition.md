# Data model for Citation information of the DaRUS upload

This datamodel covers the citation metadata needed to upload to DaRUS

### Citation

- title
  - Type: string
  - Description: title of the work.
- project
  - Type: string
  - Description: name of the project this work is related to.
- description
  - Type: string
  - Description: describtion of the content of the dataset.
- authors
  - Type: Author[]
  - Description: authors of this dataset.
- contact
  - Type: {name:string, affiliation:string, email:string}
  - Description: point of contact for this project.
- subject
  - Type: string[]
  - Description: domain specific subject categories that are topically relevant to the dataset.
- related_publication
  - Type: RelatedPublication
  - Description: publication related to the dataset.
- keywords
  - Type: Keyword[]
  - Description: keywords and url related to the project.
- topic_classification
  - Type: TopicClassification[]
  - Description: topic classification.


### RelatedPublication

- citation
  - Type: string
  - Description: full bibliographic citation for this related publication.
- id_type
  - Type: string
  - Description: type of digital identifier used for this publication, e.g., digital object identifier (DOI).
- id_number
  - Type: string
  - Description: identifier for the selected ID type.
- url
  - Type: string
  - Description: link to the publication web page, e.g., journal article page, archive record page, or other.


### Keyword

- value
  - Type: string
  - Description: key terms describing important aspects of the dataset. 
- vocabulary
  - Type: string
  - Description: for the specification of the keyword controlled vocabulary in use, such as LCSH, MeSH, or others.
- vocabulary_uri
  - Type: string
  - Description: keyword vocabulary URI points to the web presence that describes the keyword vocabulary, if appropriate.


### TopicClassification

- value
  - Type: string
  - Description: topic or Subject term that is relevant to this Dataset.
- vocab
  - Type: string
  - Description: provided for specification of the controlled vocabulary in use, e.g., LCSH, MeSH, etc.
- vocab_uri
  - Type: string
  - Description: specifies the URI location for the full controlled vocabulary.
