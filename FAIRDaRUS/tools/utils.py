
import ipywidgets as widgets
from datetime import datetime
from easyDataverse.dataset import Dataset

class citation_widget:
    """
    Widget to fill in relevant citation meta data
    """
    def __init__(self):
        
        DaRUS_subjects = ['Agricultural Sciences', 'Arts and Humanities', 'Astronomy and Astrophysics', 
                          'Business and Management', 'Chemistry', 'Computer and Information Science', 
                          'Earth and Environmental Sciences', 'Engineering', 'Law', 'Mathematical Sciences', 
                          'Medicine, Health and Life Sciences', 'Physics', 'Social Sciences', 'Other']

        self.title               = widgets.Text(description="Title of the project:",
                                                placeholder="Type the title of the project",
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})

        self.description         = widgets.Text(description="Description of the project:",
                                                placeholder="Describe the project",
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})

        self.project             = widgets.Text(description="Project:",
                                                placeholder="Name of the project group (e.g.: Project B07)",
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})

        self.authors             = widgets.Text(description="Author list:",
                                                placeholder="Name the authors of the project (e.g.: author1, author2, ...)",
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})

        self.affiliations        = widgets.Text(description="Affiliations:",
                                                placeholder="Name the affiliation fo each author (e.g.: University of Stuttgart, TUM, ...)",
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})


        self.identifier_scheme   = widgets.Dropdown(options= ["ORCID"],
                                                    description="Choose unique identifier scheme:",
                                                    layout=widgets.Layout(width='auto'),
                                                    style={'description_width': 'auto'})
        
        self.identifier          = widgets.Text(description="Unique identifier:",
                                                placeholder="Provide identifier according to choosen identifier scheme (e.g. for ORCID: xxxx-xxxx-xxxx-xxxx) for every author",
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})

        self.contact_text      = widgets.Text(description="Contact:",
                                                placeholder="Name the contact of the project (e.g.: Max Mustermann, max.mustermann@universityofstuttgart.de)",
                                                layout=widgets.Layout(width='auto'),
                                                style={'description_width': 'auto'})

        self.subject_selection   = widgets.SelectMultiple( options=DaRUS_subjects,
                                                          description="Choose subjects (press and hold 'strg' to select several):",
                                                          value=["Chemistry"],
                                                          layout=widgets.Layout(width='auto'),
                                                           style={'description_width': 'auto'} )
        
        self.related_publication  = widgets.Text (description="Related publication:",
                                                    placeholder="The full bibliographic citation for this related publication and link to the publication web page, separated by a comma (e.g.: M. Mustermann Publication: self. J. Chem. Phys. xxx, xxx (xxx), https://doi.org/xxx )",
                                                    layout=widgets.Layout(width='auto'),
                                                    style={'description_width': 'auto'})
        

        self.topic_classification = widgets.Text (description="Topic classification:",
                                                    placeholder="[Optional] The classification and the url, seperated by a comma (e.g.: homogeneous catalysis (LCSH), https://xxx, polyethers (LCSH), https://xxx, ... )",
                                                    layout=widgets.Layout(width='auto'),
                                                    style={'description_width': 'auto'})

        self.keywords             = widgets.Text (description="Keywords:",
                                                    placeholder="[Optional] The keywords and the url, seperated by a comma (e.g.: polymer chemistry (Loterre Chemistry Vocabulary), https://xxx )",
                                                    layout=widgets.Layout(width='auto'),
                                                    style={'description_width': 'auto'})

        # Widgets
        v_space   = widgets.VBox([widgets.Label(value='')], layout=widgets.Layout(height='30px'))

        widgets0  = widgets.VBox([self.title, self.description, self.project,v_space])
        widgets1  = widgets.VBox([self.authors, self.affiliations, self.contact_text, v_space, self.identifier_scheme, self.identifier, v_space])
        widgets2  = widgets.VBox([self.subject_selection, self.related_publication, self.topic_classification, self.keywords, v_space])

        # Combine the layout
        self.full_layout = widgets.VBox([widgets0, widgets1, widgets2])

    def prefill(self, dataset: Dataset):
        """
        Function that takes a Dataverse dataset and prefills the citation widgets

        Args:
            dataset (Dataset): Dataverse dataset.
        """

        self.title.value = dataset.citation.title
        self.description.value = dataset.citation.ds_description[0].value if dataset.citation.ds_description else ""
        self.project.value = dataset.citation.project[0].name if dataset.citation.project else ""

        for author in dataset.citation.author:
            self.authors.value = f"{self.authors.value}, {author.name}" if self.authors.value else author.name
            self.affiliations.value = f"{self.affiliations.value}, {author.affiliation}" if self.affiliations.value else str(author.affiliation)
            self.identifier.value = (f"{self.identifier.value}, {author.identifier}" if author.identifier_scheme == self.identifier_scheme.value
                                    and self.identifier.value else str(author.identifier) if author.identifier_scheme == self.identifier_scheme.value else "")

        self.contact_text.value = f"{dataset.citation.dataset_contact[0].name}, {dataset.citation.dataset_contact[0].email}" if dataset.citation.dataset_contact else ""

        self.subject_selection.value = dataset.citation.subject

        for keyword in dataset.citation.keyword:
            self.keywords.value = ( f"{self.keywords.value}, {keyword.value}, {keyword.vocabulary_uri}" if self.keywords.value else 
                                   f"{keyword.value}, {keyword.vocabulary_uri}")

        for topic in dataset.citation.topic_classification:
            self.topic_classification.value = ( f"{self.topic_classification.value}, {topic.value}, {topic.vocab_uri}" if self.topic_classification.value else 
                                                f"{topic.value}, {topic.vocab_uri}")

        self.related_publication.value = f"{dataset.citation.publication[0].citation}, {dataset.citation.publication[0].url}" if dataset.citation.publication else ""

    def save_input(self, dataset: Dataset, depositor: str):

        # Add project group
        dataset.citation.project = []
        dataset.citation.add_project( name = self.project.value, level="1" )
        
        # Add title
        dataset.citation.title = self.title.value
        
        # Add description
        dataset.citation.ds_description = []
        dataset.citation.add_ds_description( value = self.description.value )

        # Add authors to the dataset 
        dataset.citation.author = []
        for aut,aff,ident in zip( self.authors.value.split(","), self.affiliations.value.split(","), self.identifier.value.split(",") ):
            dataset.citation.add_author( name = aut.strip(), 
                                         affiliation = aff.strip(), 
                                         identifier_scheme = self.identifier_scheme.value,
                                         identifier = ident.strip() ) 

        # Add point of contact
        dataset.citation.dataset_contact = []
        dataset.citation.add_dataset_contact( name = self.contact_text.value.split(",")[0].strip(), 
                                              email = self.contact_text.value.split(",")[1].strip() ) 

        # Add subjects
        dataset.citation.subject      = self.subject_selection.value

        # Add depositor
        dataset.citation.depositor       = depositor
        dataset.citation.date_of_deposit = datetime.now().date().strftime("%Y-%m-%d")
        
        # Add generall SFB information
        dataset.citation.grant_number = []
        dataset.citation.add_grant_number( agency="DFG", value="358283783 - SFB 1333")

        # Add language
        dataset.citation.language     = [ "English" ]

        # Add related publication
        dataset.citation.publication = []
        dataset.citation.add_publication( citation = self.related_publication.value.split(",")[0].strip(),
                                          url      = self.related_publication.value.split(",")[1].strip() )
        
        # Add topic classification (if provided)
        dataset.topic_classification = []
        if self.topic_classification.value:
            for i in range(0, len(self.topic_classification.value.split(",")), 2):
                dataset.citation.add_topic_classification( value     = self.topic_classification.value.split(",")[i].strip() , 
                                                           vocab_uri = self.topic_classification.value.split(",")[i + 1].strip() )

        # Add keywords
        dataset.citation.keyword = []
        if self.keywords.value:
            for i in range(0, len(self.keywords.value.split(",")), 2):
                dataset.citation.add_keyword( value          = self.keywords.value.split(",")[i].strip() , 
                                              vocabulary_uri = self.keywords.value.split(",")[i + 1].strip() )