# Data model for Citation information of the DaRUS upload

This datamodel covers the citation metadata needed to upload to DaRUS

## Objects

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


### Author

- name
  - Type: string
  - Description: full name including given and family name.
- affiliation
  - Type: string
  - Description: organization the author is affiliated to.