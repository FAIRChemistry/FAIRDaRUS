import ipywidgets as widgets
from datetime import datetime
from easyDataverse.dataset import Dataset


class citation_widget:
    """
    Widget to fill in relevant citation meta data
    """

    def __init__(self):
        DaRUS_subjects = [
            "Agricultural Sciences",
            "Arts and Humanities",
            "Astronomy and Astrophysics",
            "Business and Management",
            "Chemistry",
            "Computer and Information Science",
            "Earth and Environmental Sciences",
            "Engineering",
            "Law",
            "Mathematical Sciences",
            "Medicine, Health and Life Sciences",
            "Physics",
            "Social Sciences",
            "Other",
        ]

        self.title = widgets.Text(
            description="Title of the project:",
            placeholder="Type the title of the project",
            layout=widgets.Layout(width="auto"),
            style={"description_width": "auto"},
        )

        self.description = widgets.Text(
            description="Description of the project:",
            placeholder="Describe the project",
            layout=widgets.Layout(width="auto"),
            style={"description_width": "auto"},
        )

        self.authors = widgets.Text(
            description="Author list:",
            placeholder="Name the authors of the project (e.g.: author1, author2, ...)",
            layout=widgets.Layout(width="auto"),
            style={"description_width": "auto"},
        )

        self.affiliations = widgets.Text(
            description="Affiliations:",
            placeholder="Name the affiliation fo each author (e.g.: University of Stuttgart, TUM, ...)",
            layout=widgets.Layout(width="auto"),
            style={"description_width": "auto"},
        )

        self.contact_text = widgets.Text(
            description="Contact:",
            placeholder="Name the contact of the project (e.g.: Max Mustermann, max.mustermann@universityofstuttgart.de)",
            layout=widgets.Layout(width="auto"),
            style={"description_width": "auto"},
        )

        self.subject_selection = widgets.SelectMultiple(
            options=DaRUS_subjects,
            description="Choose subjects (press and hold 'strg' to select several):",
            value=["Chemistry"],
            layout=widgets.Layout(width="auto"),
            style={"description_width": "auto"},
        )

        # Widgets
        v_space = widgets.VBox(
            [widgets.Label(value="")], layout=widgets.Layout(height="30px")
        )

        widgets0 = widgets.VBox([self.title, self.description, v_space])
        widgets1 = widgets.VBox(
            [
                self.authors,
                self.affiliations,
                self.contact_text,
                v_space,
                self.subject_selection,
            ]
        )

        # Combine the layout
        self.full_layout = widgets.VBox([widgets0, widgets1])

    def prefill(self, dataset: Dataset):
        """
        Function that takes a Dataverse dataset and prefills the citation widgets

        Args:
            dataset (Dataset): Dataverse dataset.
        """

        self.title.value = dataset.citation.title
        self.description.value = (
            dataset.citation.ds_description[0].value
            if dataset.citation.ds_description
            else ""
        )

        for author in dataset.citation.author:
            self.authors.value = (
                f"{self.authors.value}, {author.name}"
                if self.authors.value
                else author.name
            )
            self.affiliations.value = (
                f"{self.affiliations.value}, {author.affiliation}"
                if self.affiliations.value
                else str(author.affiliation)
            )

        self.contact_text.value = (
            f"{dataset.citation.dataset_contact[0].name}, {dataset.citation.dataset_contact[0].email}"
            if dataset.citation.dataset_contact
            else ""
        )

        self.subject_selection.value = dataset.citation.subject


    def save_input(self, dataset: Dataset, depositor: str):

        # Add title
        dataset.citation.title = self.title.value

        # Add description
        dataset.citation.ds_description = []
        dataset.citation.add_ds_description(value=self.description.value)

        # Add authors to the dataset
        dataset.citation.author = []
        for aut, aff in zip(
            self.authors.value.split(","),
            self.affiliations.value.split(",")
        ):
            dataset.citation.add_author(
                name=aut.strip(),
                affiliation=aff.strip()
            )

        # Add point of contact
        dataset.citation.dataset_contact = []
        dataset.citation.add_dataset_contact(
            name=self.contact_text.value.split(",")[0].strip(),
            email=self.contact_text.value.split(",")[1].strip(),
        )

        # Add subjects
        dataset.citation.subject = self.subject_selection.value

        # Add depositor
        dataset.citation.depositor = depositor
        dataset.citation.date_of_deposit = datetime.now().date().strftime("%Y-%m-%d")

        # Add generall SFB information
        dataset.citation.grant_number = []
        dataset.citation.add_grant_number(agency="DFG", value="358283783 - SFB 1333")

        # Add language
        dataset.citation.language = ["English"]
