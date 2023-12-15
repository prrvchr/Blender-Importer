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

""" Gui workbench initialization """


class BlenderImporter(Workbench):

    MenuText = 'Blender Importer'
    ToolTip =  'Blender Importer workbench'
    Icon = '''
/* XPM */
static char * blender_xpm[] = {
"32 29 2 1",
" 	c None",
".	c #000000",
"           ..                   ",
"          .....                 ",
"           ......               ",
"            ........            ",
"              .......           ",
"               ........         ",
" ........................       ",
"..........................      ",
"............................    ",
" ............................   ",
"          ........    ........  ",
"         .......         .....  ",
"       ........    ...    ..... ",
"     .........   .......  ..... ",
"    ..........  ........   .....",
"  ...........   .........  .....",
" ............  ..........   ....",
".............  ..........   ....",
"........ ....  ..........  .....",
".......  ....   .........  .....",
" .....   .....  ........   .... ",
"  ..      ....   ......   ..... ",
"          .....          ...... ",
"           .....        ......  ",
"           ........   .......   ",
"            .................   ",
"             ...............    ",
"               ...........      ",
"                 .......        "};
'''

    def Initialize(self):
        import FreeCAD as App
        import FreeCADGui as Gui
        from bimp import BlenderImport, MakeMaterial, ApplyMaterial, EditMaterial
        import bpy
        Gui.addCommand('Blender_Import', BlenderImport())
        Gui.addCommand('Make_Material',  MakeMaterial())
        Gui.addCommand('Apply_Material', ApplyMaterial())
        Gui.addCommand('Edit_Material',  EditMaterial())
        commands = ['Blender_Import', 'Make_Material', 'Apply_Material', 'Edit_Material']
        # Add commands to menu and toolbar
        self.appendToolbar("Blender Importer v0.0.2", commands)
        App.Console.PrintMessage(f"Initialize pby version is: {bpy.app.version_string}\n")

    def GetClassName(self):
        return 'Gui::PythonWorkbench'

    def Activated(self):
        import FreeCAD as App
        App.Console.PrintMessage("BlenderImporter workbench activated\n")

    def Deactivated(self):
        import FreeCAD as App
        App.Console.PrintMessage("BlenderImporter workbench deactivated\n")


Gui.addWorkbench(BlenderImporter())
