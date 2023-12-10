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

""" Blender material edit object """

import FreeCAD as App
import FreeCADGui as Gui

from PySide.QtGui import QFormLayout, QComboBox, QListWidget, QPushButton, QLayout

from .helper import isValidMaterial

import os, json

uipath = os.path.dirname(__file__)
uidir  = 'ui'


class BlenderMaterial:
    def __init__(self, obj=None):
        # Initialize task panel
        self._root = 'Blender'
        self._deleted = []
        taskpage = os.path.join(uipath , uidir, 'BlenderMaterial.ui')
        self.form = Gui.PySideUic.loadUi(taskpage)

        # Initialize material name combo
        self._combo = self.form.findChild(QComboBox, "comboBox")
        self._list = self.form.findChild(QListWidget, "listWidget")
        self._button = self.form.findChild(QPushButton, "pushButton")
        self._materials = {obj.Label: obj
                           for obj in App.ActiveDocument.Objects
                           if isValidMaterial(obj)}

        self._combo.addItems(list(self._materials.keys()))
        selection = [obj.Label for obj in Gui.Selection.getSelection()]
        if selection:
            self._combo.setCurrentText(selection[0])
        if self._combo.currentIndex() != -1:
            self._loadSockets(self._combo.currentText())

        self._combo.currentTextChanged.connect(self.onMaterialChanched)
        self._button.clicked.connect(self.onButtonClicked)

    def accept(self):
        # Respond to user acceptation (OK button)
        for material in self._deleted:
            self._deleteSockets(material)
        Gui.ActiveDocument.resetEdit()
        Gui.Control.closeDialog()
        # Modifying material may require projects recomputation:
        if self._deleted:
            App.ActiveDocument.recompute()
        return True

    def onMaterialChanched(self, material):
        self._list.clear()
        if material in self._deleted:
            self._button.setEnabled(False)
        else:
            self._loadSockets(material)

    def onButtonClicked(self):
        self._deleted.append(self._combo.currentText())
        self._list.clear()
        self._button.setEnabled(False)

    def _loadSockets(self, material):
        data = self._materials[material].Material.get(self._root)
        if data:
            self._list.addItems(json.loads(data))
            self._button.setEnabled(True)
        else:
            self._button.setEnabled(False)

    def _deleteSockets(self, name):
        material = self._materials[name].Material.copy()
        data = material[self._root]
        if data:
            for socket in json.loads(data):
                del(material[self._root + '.' + socket])
        del(material[self._root])
        self._materials[name].Material = material
