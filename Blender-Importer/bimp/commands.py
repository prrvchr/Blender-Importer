#!
# -*- coding: utf-8 -*-

'''
╔════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                    ║
║   Copyright (c) 2020 https://prrvchr.github.io                                     ║
║                                                                                    ║
║   Permission is hereby granted, free of charge, to any person obtaining            ║
║   a copy of this software and associated documentation files (the "Software"),     ║
║   to deal in the Software without restriction, including without limitation        ║
║   the rights to use, copy, modify, merge, publish, distribute, sublicense,         ║
║   and/or sell copies of the Software, and to permit persons to whom the Software   ║
║   is furnished to do so, subject to the following conditions:                      ║
║                                                                                    ║
║   The above copyright notice and this permission notice shall be included in       ║
║   all copies or substantial portions of the Software.                              ║
║                                                                                    ║
║   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,                  ║
║   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES                  ║
║   OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.        ║
║   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY             ║
║   CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,             ║
║   TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE       ║
║   OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                                    ║
║                                                                                    ║
╚════════════════════════════════════════════════════════════════════════════════════╝
'''

""" Blender command object """

import FreeCAD as App
import FreeCADGui as Gui

from PySide2.QtWidgets import QFileDialog
from PySide.QtGui import QMessageBox, QInputDialog

import os

from ArchMaterial import _CommandArchMaterial

from .taskpanels import BlenderMaterial

from .helper import importFile, isMultiMaterial

iconpath = os.path.dirname(__file__)
icondir  = 'icons'


class BlenderImport():

    def GetResources(self):
        icon = os.path.join(iconpath , icondir, 'blender-importer.svg')
        return {'Pixmap':   icon,
                'MenuText': 'Blender Import',
                'Accel':    'B, I',
                'ToolTip':  'Import Blender file'}

    def IsActive(self):
        return True

    def Activated(self):
        doc = App.ActiveDocument
        if doc is None:
            App.Console.PrintMessage("\n")
            App.Console.PrintMessage("No document open, can't continue...\n")
            return
        if not doc.FileName:
            App.Console.PrintMessage("\n")
            App.Console.PrintMessage("The active document has not been saved, can't continue...\n")
            return
        doc.openTransaction('Blender Import')
        success, warnings, url = importFile(doc)
        doc.commitTransaction()
        doc.recompute()
        if success:
            path, filename = os.path.split(url)
            App.Console.PrintMessage("\n")
            for msg in warnings:
                App.Console.PrintMessage(msg)
            App.Console.PrintMessage(f"File import: {filename} ended with {len(warnings)} warnings\n")


class MakeMaterial(_CommandArchMaterial):

    def GetResources(self):
        resource = super().GetResources()
        resource['MenuText'] = 'Blender Material'
        resource['Accel'] =    'B, M'
        resource['ToolTip'] =  'Create Blender material'
        return resource

    def IsActive(self):
        return True

    def Activated(self):
        App.ActiveDocument.openTransaction("Blender Material")
        Gui.Control.closeDialog()
        Gui.addModule("ArchMaterial")
        cmds = ["obj = ArchMaterial.makeMaterial()",
                "Gui.Selection.clearSelection()",
                "Gui.Selection.addSelection(obj.Document.Name, obj.Name)",
                "obj.ViewObject.Document.setEdit(obj.ViewObject, 0)"]
        for cmd in cmds:
            Gui.doCommand(cmd)
        App.ActiveDocument.commitTransaction()


class ApplyMaterial():
    """GUI command to apply a material to an object."""

    def GetResources(self):
        icon = os.path.join(iconpath , icondir, 'ApplyMaterial.svg')
        return {'Pixmap':   icon,
                'MenuText': 'Apply Material',
                'Accel':    'A, M',
                'ToolTip':  'Apply a Material to selection'}

    def Activated(self):
        """Respond to Activated event (callback).

        This code is executed when the command is run in FreeCAD.
        It sets the Material property of the selected object(s).
        If the Material property does not exist in the object(s), it is
        created.
        """
        # Get selected objects
        selection = Gui.Selection.getSelection()
        if not selection:
            title = 'Blender Importer empty Selection'
            msg = 'Please select object(s) before applying material.'
            QMessageBox.warning(None, title, msg)
            return

        # Let user pick the Material
        mats = [o for o in App.ActiveDocument.Objects
                if o.isDerivedFrom("App::MaterialObjectPython") or isMultiMaterial(o)]
        if not mats:
            title = 'Blender Importer no Material'
            msg = 'No Material in document. Please create a Material before applying.'
            QMessageBox.warning(None, title, msg)
            return

        matlabels = [m.Label for m in mats]
        current_mats_labels = [
            o.Material.Label
            for o in selection
            if hasattr(o, "Material")
            and hasattr(o.Material, "Label")
            and o.Material.Label
        ]
        current_mats = [
            count
            for count, val in enumerate(matlabels)
            if val in current_mats_labels
        ]
        current_mat = current_mats[0] if len(current_mats) == 1 else 0

        input, status = QInputDialog.getItem(None,
                                             'Blender Importer Material Applier',
                                             'Choose Material to apply to selection:',
                                             matlabels,
                                             current_mat,
                                             False)
        if not status:
            return

        material = next(m for m in mats if m.Label == input)

        # Update selected objects
        App.ActiveDocument.openTransaction('MaterialApplier')
        for obj in selection:
            # Add Material property to the object if it hasn't got one
            if 'Material' not in obj.PropertiesList:
                obj.addProperty('App::PropertyLink', 'Material', '', 'The Material for this object')
            try:
                obj.Material = material
            except TypeError:
                msg = f'Cannot apply Material to object: {obj.Label}, material property is of wrong type'
                App.Console.PrintError(msg)
        App.ActiveDocument.commitTransaction()


class EditMaterial():
    """GUI command to view Blender settings of a material object."""

    def GetResources(self):
        icon = os.path.join(iconpath , icondir, 'EditMaterial.svg')
        return {'Pixmap':   icon,
                'MenuText': 'Edit Material',
                'Accel':    'E, M',
                'ToolTip':  'Edit a Blender Material'}

    def Activated(self):
        """This code is executed when the command is run in FreeCAD.
        It opens a dialog to view / delete Blender nodes of the selected
        material.
        """
        App.ActiveDocument.openTransaction("EditMaterial")
        task = BlenderMaterial()
        Gui.Control.showDialog(task)
        App.ActiveDocument.commitTransaction()
