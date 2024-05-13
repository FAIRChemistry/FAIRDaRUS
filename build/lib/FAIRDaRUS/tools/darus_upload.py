#!~/miniconda3/bin/python

import os
import ipywidgets as widgets

from typing import List
from datetime import datetime
from easyDataverse import Dataverse
from IPython.display import display, clear_output

from .utils import citation_widget

# Other #
# Mute the "libuv only supports millisecond timer resolution" warning
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="gevent.hub")


class DaRUS_upload:
    def action_handler(self, _):
        with self.action_output:
            clear_output(wait=True)

            if len(self.api_token_text.value.split("-")) == 5:
                self.dataverse = Dataverse(
                    server_url="https://darus.uni-stuttgart.de",
                    api_token=self.api_token_text.value,
                )
            else:
                raise KeyError("Invalid API token presented\n")

            if self.action_dropdown.value == "Create new one":
                self.create_new()

            elif self.action_dropdown.value == "Edit existing one":
                self.edit_existing()

            else:
                # Print empty space to overwrite existing widget output
                print("")

    def add_file_dir(self, _):
        # Clear previous output and print the new message in the button's output area
        flag = False
        with self.button_output:
            clear_output(wait=True)
            if os.path.isfile(self.file_directoy_input.value) or os.path.isdir(
                self.file_directoy_input.value
            ):
                if os.path.isdir(self.file_directoy_input.value):
                    flag = True
                    self.DaRUS_data.add_directory(
                        dirpath=self.file_directoy_input.value
                    )
                elif os.path.isfile(self.file_directoy_input.value):
                    self.DaRUS_data.add_file(
                        local_path=self.file_directoy_input.value,
                        description=self.file_description_input.value,
                    )

                print(f"Added file / directory: {self.file_directoy_input.value }")
            else:
                print(
                    f"The specified entry is neither a file nor a directory:\n {self.file_directoy_input.value}"
                )

        # If directory is added, add description to every file manually
        if flag:
            for file in self.DaRUS_data.files:
                if self.file_directoy_input.value in file.filepath:
                    file.description = self.file_description_input.value

        # Update file / dir widget
        self.file_directoy.value = [file.filepath for file in self.DaRUS_data.files]

        # Reset file and description
        self.file_directoy_input.value = ""
        self.file_description_input.value = ""

    def files_dir_handler(self, _):
        # Delete files / directories that are not in the files / directories widget anymore
        del_idx = [
            i
            for i, file in enumerate(self.DaRUS_data.files)
            if not file.filepath in self.file_directoy.value
        ]
        del_idx.sort(reverse=True)

        for idx in del_idx:
            del self.DaRUS_data.files[idx]

        self.file_directoy.value = [file.filepath for file in self.DaRUS_data.files]

    def create_new(self):
        # Create new DaRUS dataset
        self.DaRUS_data = self.dataverse.create_dataset()

        self.dataverse_dropdown = widgets.Dropdown(
            options=self.dataverse_list,
            description="Choose dataverse:",
            layout=widgets.Layout(width="auto"),
            style={"description_width": "auto"},
        )

        # Handle button
        self.button_upload.on_click(self.upload_to_DaRUS)

        # Widgets
        v_space = widgets.VBox(
            [widgets.Label(value="")], layout=widgets.Layout(height="30px")
        )

        widgets0 = widgets.VBox([v_space, self.citation.full_layout, v_space])
        widgets1 = widgets.VBox([self.dataverse_dropdown, v_space])
        widgets2 = widgets.VBox([self.file_directoy_input, self.file_description_input])
        widgets3 = widgets.VBox(
            [self.button_add_file_dir, self.button_output],
            layout=widgets.Layout(align_items="center"),
        )
        widgets4 = widgets.VBox(
            [
                v_space,
                widgets.Label(value="Files / directories in DaRUS dataset:"),
                self.file_directoy,
            ]
        )
        widgets5 = widgets.VBox(
            [self.button_upload], layout=widgets.Layout(align_items="center")
        )

        # Combine the layout
        full_layout = widgets.VBox(
            [widgets0, widgets1, widgets2, widgets3, widgets4, widgets5]
        )

        # Display the layout
        display(full_layout)

    def edit_existing(self):
        self.doi_text = widgets.Text(
            description="DOI/PID for dataverse:",
            placeholder="Doi of exisitng dataverse (e.g.: 'doi:xx.xxxxx/darus-xxxx)",
            layout=widgets.Layout(width="auto"),
            style={"description_width": "auto"},
        )

        self.button_download = widgets.Button(
            description="Download dataset from DaRUS",
            layout=widgets.Layout(width="30%"),
            style={"button_color": "lightblue"},
        )

        self.file_directoy_text = widgets.Text(
            description="Destination directory",
            placeholder="Destination directory for DaRUS download. E.g: current directory with '.' ",
            layout=widgets.Layout(width="auto"),
            style={"description_width": "auto"},
        )

        # Handle button
        self.button_download.on_click(self.download_from_DaRUS)

        v_space = widgets.VBox(
            [widgets.Label(value="")], layout=widgets.Layout(height="30px")
        )
        widgets0 = widgets.VBox(
            [
                self.doi_text,
                self.file_directoy_text,
            ]
        )
        widgets1 = widgets.VBox(
            [v_space, self.button_download], layout=widgets.Layout(align_items="center")
        )

        # Combine the layout
        full_layout = widgets.VBox([widgets0, widgets1, v_space, self.download_output])

        # Display the layout
        display(full_layout)

    def download_from_DaRUS(self, _):
        # Create folder where DaRUS data is saved
        os.makedirs(
            os.path.dirname(os.getcwd() + "/" + self.file_directoy_text.value),
            exist_ok=True,
        )

        # Load existing DaRUS dataset
        self.DaRUS_data = self.dataverse.load_dataset(
            self.doi_text.value, filedir=self.file_directoy_text.value
        )

        # Initialize
        self.file_directoy.value = [file.filepath for file in self.DaRUS_data.files]

        # Fill out citation widget with preexisting data
        self.citation.prefill(dataset=self.DaRUS_data)

        # Handle button
        self.button_upload.on_click(self.update_to_DaRUS)

        with self.download_output:
            clear_output(wait=True)
            v_space = widgets.VBox(
                [widgets.Label(value="")], layout=widgets.Layout(height="30px")
            )

            widgets0 = widgets.VBox([v_space, self.citation.full_layout, v_space])
            widgets1 = widgets.VBox(
                [self.file_directoy_input, self.file_description_input]
            )
            widgets2 = widgets.VBox(
                [self.button_add_file_dir, self.button_output],
                layout=widgets.Layout(align_items="center"),
            )
            widgets3 = widgets.VBox(
                [
                    v_space,
                    widgets.Label(value="Files / directories in DaRUS dataset:"),
                    self.file_directoy,
                ]
            )
            widgets4 = widgets.VBox(
                [self.button_upload], layout=widgets.Layout(align_items="center")
            )

            # Combine the layout
            full_layout = widgets.VBox(
                [widgets0, widgets1, widgets2, widgets3, widgets4]
            )

            # Display the layout
            display(full_layout)

    def update_to_DaRUS(self, _):
        # Update citation metadata from widget
        self.citation.save_input(
            dataset=self.DaRUS_data, depositor=self.depositor_text.value
        )

        # Update dataset
        self.DaRUS_data.update()

        # Initialize
        self.file_directoy.value = []

    def upload_to_DaRUS(self, _):
        """
        Function that uses the provided sdRDM dataset to extract all necessary information to upload a dataset to DaRUS.
        """

        # Fill in citation metadata from widget
        self.citation.save_input(
            dataset=self.DaRUS_data, depositor=self.depositor_text.value
        )

        # Upload dataset
        self.DaRUS_data.upload(dataverse_name=self.dataverse_dropdown.value)

        # Initialize
        self.file_directoy.value = []

    def DaRUS(self, dataverse_list: List):
        # Common variables
        self.dataverse_list = dataverse_list

        # Common widgets
        self.file_directoy_input = widgets.Text(
            description="Path to file / directory (can be absolut or relative):",
            placeholder="Addiotional directories or paths that should be uploaded, only one entry allowed (e.g.: ./data/Rohdaten, ./data/calibration/calibration.json, ... )",
            layout=widgets.Layout(width="auto"),
            style={"description_width": "auto"},
        )

        self.file_description_input = widgets.Text(
            description="Description of the file / directory:",
            placeholder="Addiotional description of the file / directory.",
            layout=widgets.Layout(width="auto"),
            style={"description_width": "auto"},
        )

        self.file_directoy = widgets.TagsInput(allow_duplicates=False)

        self.button_add_file_dir = widgets.Button(
            description="Add file / directory to DaRUS dataset",
            layout=widgets.Layout(width="30%"),
        )

        self.button_upload = widgets.Button(
            description="Upload dataset to DaRUS",
            layout=widgets.Layout(width="30%"),
            style={"button_color": "lightblue"},
        )

        # Define output spaces
        self.button_output = widgets.Output()
        self.download_output = widgets.Output()
        self.action_output = widgets.Output()

        # Handle buttons
        self.button_add_file_dir.on_click(self.add_file_dir)

        # Main widgets
        self.action_dropdown = widgets.Dropdown(
            options=["", "Create new one", "Edit existing one"],
            description="Choose whether you want to create a new data record or edit an existing one:",
            layout=widgets.Layout(width="auto"),
            style={"description_width": "auto"},
        )

        self.depositor_text = widgets.Text(
            description="Depositor:",
            placeholder="Name of the person uploading this dataset (e.g.: Max Mustermann)",
            layout=widgets.Layout(width="auto"),
            style={"description_width": "auto"},
        )

        self.api_token_text = widgets.Text(
            description="API token:",
            placeholder="Provide personal API token for DaRUS (e.g.: xxx-xxx-xxx-xxx-xxx)",
            layout=widgets.Layout(width="auto"),
            style={"description_width": "auto"},
        )

        # Handle effects
        self.action_dropdown.observe(self.action_handler)
        self.file_directoy.observe(self.files_dir_handler)

        # Citation widget
        self.citation = citation_widget()

        # Display general widgets
        v_space = widgets.VBox(
            [widgets.Label(value="")], layout=widgets.Layout(height="30px")
        )
        display(
            widgets.VBox(
                [
                    self.action_dropdown,
                    self.depositor_text,
                    self.api_token_text,
                    v_space,
                    self.action_output,
                ]
            )
        )
