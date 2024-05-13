```mermaid
classDiagram
    Citation *-- Author
    
    class Citation {
        +string title
        +string project
        +string description
        +Author[0..*] authors
        +Contact contact
        +string[0..*] subject
    }
    
    class Author {
        +string name
        +string affiliation
    }
    
```