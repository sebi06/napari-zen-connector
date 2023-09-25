# -*- coding: utf-8 -*-

#################################################################
# File        : dock_widget.py
# Author      : sebi06
#
# Disclaimer: This code is purely experimental. Feel free to
# use it at your own risk.
#
# Remarks: Requires ???
#################################################################


import numpy as np
from napari.layers import Labels, Image
from pathlib import Path
import os
from typing import Dict, List, Tuple, Union
from qtpy.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QDialogButtonBox,
    QSlider,
    QTableWidget,
    QTableWidgetItem,
    QSizePolicy,
)

from qtpy.QtCore import Qt, Signal, QObject, QEvent, QSize
from qtpy.QtGui import QFont
from magicgui.widgets import (
    FileEdit,
    PushButton,
    Slider,
    Container,
    Label,
    CheckBox,
    LineEdit,
    Select,
    ComboBox,
)
from magicgui.types import FileDialogMode

from .zencontrol import ZenExperiment, ZenDocuments


class TableWidget(QWidget):
    def __init__(self) -> None:
        super(QWidget, self).__init__()

        self.layout = QVBoxLayout(self)
        self.model_table = QTableWidget()

        self.model_table.setShowGrid(True)
        self.model_table.setHorizontalHeaderLabels(["Parameter", "Value"])
        # self.model_table.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        header = self.model_table.horizontalHeader()
        header.setDefaultAlignment(Qt.AlignLeft)
        self.layout.addWidget(self.model_table)

    def update_model_metadata(self, md_dict: Dict) -> None:
        # number of rows is set to number of metadata entries
        row_count = len(md_dict)
        col_count = 2
        self.model_table.setColumnCount(col_count)
        self.model_table.setRowCount(row_count)

        row = 0

        # update the table with the entries from metadata dictionary
        for key, value in md_dict.items():
            newkey = QTableWidgetItem(key)
            self.model_table.setItem(row, 0, newkey)
            newvalue = QTableWidgetItem(str(value))
            self.model_table.setItem(row, 1, newvalue)
            row += 1

        # fit columns and rows to content
        self.model_table.resizeColumnsToContents()
        self.model_table.resizeRowsToContents()
        self.model_table.adjustSize()

    def update_style(self) -> None:
        # define font size and type
        fnt = QFont()
        fnt.setPointSize(8)
        fnt.setBold(True)
        fnt.setFamily("Arial")

        # update both header items
        fc = (25, 25, 25)
        # item1 = QtWidgets.QTableWidgetItem("Parameter")
        item1 = QTableWidgetItem("Parameter")
        # item1.setForeground(QtGui.QColor(25, 25, 25))
        item1.setFont(fnt)
        self.model_table.setHorizontalHeaderItem(0, item1)

        # item2 = QtWidgets.QTableWidgetItem("Value")
        item2 = QTableWidgetItem("Value")
        # item2.setForeground(QtGui.QColor(25, 25, 25))
        item2.setFont(fnt)
        self.model_table.setHorizontalHeaderItem(1, item2)


# our manifest widget command points to this class
class connect_zen(QWidget):
    """Widget allows to connect to ZEN and select an ZenExperiment (*.czexp) to be executed.
    Optionally the CZI image can be opened inside Napari.

    """

    def __init__(self, napari_viewer):
        """Initialize widget
        Parameters
        ----------
        napari_viewer : napari.utils._proxies.PublicOnlyProxy
            public proxy for the napari viewer object
        """
        super().__init__()
        self.viewer = napari_viewer

        self.expfolder_default = Path(r"f:\Documents\Carl Zeiss\ZEN\Documents\Experiment Setups")

        # create a layout
        self.setLayout(QVBoxLayout())

        # add a text file where one can enter the default location for the experiment files
        self.layout().addWidget(QLabel("Define ZenExperiment Folder"))
        self.expfolder = LineEdit(value=self.expfolder_default)
        self.layout().addWidget(self.expfolder.native)

        # check if directory exists
        if os.path.isdir(self.expfolder_default):
            print("ZEN Experiment Setups Folder :", self.expfolder_default, "found.")

            # get lists with existing experiment files
            self.expdocs = ZenDocuments()
            self.expfiles_long, self.expfiles_short = self.expdocs.getfilenames(
                folder=self.expfolder_default, pattern="*.czexp"
            )

        if not os.path.isdir(self.expfolder_default):
            print("ZEN Experiment Setups Folder :", self.expfolder_default, "not found.")

        self.layout().addWidget(QLabel("Select ZEN Experiment"))
        self.expselect = QComboBox(self)
        self.expselect.addItems(self.expfiles_short)
        self.expselect.setStyleSheet("font: bold;" "font-size: 10px;")
        self.layout().addWidget(self.expselect)

        # # create the FileEdit widget and add to the layout and connect it
        # self.experiment_edit = FileEdit(
        #     mode=FileDialogMode.EXISTING_FILE, value=self.expfolder_default, filter=model_extension
        # )

        # self.layout().addWidget(self.experiment_edit.native)

        # self.experiment_edit.line_edit.changed.connect(self._file_changed)
