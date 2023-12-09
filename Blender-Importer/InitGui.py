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
"26 34 141 2",
"  	c None",
". 	c #363636",
"+ 	c #3A3A3A",
"@ 	c #383838",
"# 	c #3B3B3B",
"$ 	c #3D3D3D",
"% 	c #888888",
"& 	c #525252",
"* 	c #797979",
"= 	c #494949",
"- 	c #5F5F5F",
"; 	c #414141",
"> 	c #323232",
", 	c #454545",
"' 	c #373737",
") 	c #565656",
"! 	c #949494",
"~ 	c #434343",
"{ 	c #5D5D5D",
"] 	c #333333",
"^ 	c #353535",
"/ 	c #404040",
"( 	c #B5B5B5",
"_ 	c #B7B7B7",
": 	c #919191",
"< 	c #AAAAAA",
"[ 	c #979797",
"} 	c #BFBFBF",
"| 	c #B6B6B6",
"1 	c #969696",
"2 	c #BEBEBE",
"3 	c #959595",
"4 	c #C6C6C6",
"5 	c #8F8F8F",
"6 	c #9A9A9A",
"7 	c #ABABAB",
"8 	c #B9B9B9",
"9 	c #9C9C9C",
"0 	c #3E3E3E",
"a 	c #B2B2B2",
"b 	c #6F6F6F",
"c 	c #C0C0C0",
"d 	c #BABABA",
"e 	c #A3A3A3",
"f 	c #A0A0A0",
"g 	c #C4C4C4",
"h 	c #9E9E9E",
"i 	c #747474",
"j 	c #BBBBBB",
"k 	c #9D9D9D",
"l 	c #A6A6A6",
"m 	c #9B9B9B",
"n 	c #4F4F4F",
"o 	c #5E5E5E",
"p 	c #737373",
"q 	c #595959",
"r 	c #575757",
"s 	c #474747",
"t 	c #777777",
"u 	c #545454",
"v 	c #606060",
"w 	c #656565",
"x 	c #4A4A4A",
"y 	c #787878",
"z 	c #6A6A6A",
"A 	c #444444",
"B 	c #757575",
"C 	c #5B5B5B",
"D 	c #616161",
"E 	c #343434",
"F 	c #B0B0B0",
"G 	c #EFEFEF",
"H 	c #7C7C7C",
"I 	c #EDEDED",
"J 	c #FCFCFC",
"K 	c #424242",
"L 	c #E3E3E3",
"M 	c #FEFEFE",
"N 	c #D9D9D9",
"O 	c #5A5A5A",
"P 	c #555555",
"Q 	c #D7D7D7",
"R 	c #E0E0E0",
"S 	c #E1E1E1",
"T 	c #E5E5E5",
"U 	c #EEEEEE",
"V 	c #FFFFFF",
"W 	c #EAEAEA",
"X 	c #838383",
"Y 	c #EBEBEB",
"Z 	c #F3F3F3",
"` 	c #FAFAFA",
" .	c #F1F1F1",
"..	c #FDFDFD",
"+.	c #2C2C2C",
"@.	c #2F2F2F",
"#.	c #DBDBDB",
"$.	c #F2F2F2",
"%.	c #4C4C4C",
"&.	c #F5F5F5",
"*.	c #8A8A8A",
"=.	c #848484",
"-.	c #ECECEC",
";.	c #7D7D7D",
">.	c #696969",
",.	c #636363",
"'.	c #ACACAC",
").	c #A9A9A9",
"!.	c #F8F8F8",
"~.	c #393939",
"{.	c #D8D8D8",
"].	c #3C3C3C",
"^.	c #7A7A7A",
"/.	c #C8C8C8",
"(.	c #FBFBFB",
"_.	c #DCDCDC",
":.	c #DDDDDD",
"<.	c #2E2E2E",
"[.	c #626262",
"}.	c #8D8D8D",
"|.	c #ADADAD",
"1.	c #E9E9E9",
"2.	c #E7E7E7",
"3.	c #7F7F7F",
"4.	c #D2D2D2",
"5.	c #E6E6E6",
"6.	c #6D6D6D",
"7.	c #646464",
"8.	c #585858",
"9.	c #2D2D2D",
"0.	c #7E7E7E",
"a.	c #CFCFCF",
"b.	c #DADADA",
"c.	c #F9F9F9",
"d.	c #303030",
"e.	c #484848",
"f.	c #C7C7C7",
"g.	c #AFAFAF",
"h.	c #F0F0F0",
"i.	c #535353",
"j.	c #4D4D4D",
"                                                    ",
"                                                    ",
"      . . . . . . . . . . . . . . . . . . . .       ",
"    . . + . . @ . . . . . . . . # . . . . . . .     ",
"    . $ % & $ * = - ; > = , ' ) ! ~ { = ] = + .     ",
"    ^ / ( ! _ : < [ } | 1 2 [ 3 4 5 6 7 8 9 0 ^     ",
"    ^ / a b c ! d e f 8 @ g h i j k l m j n . ^     ",
"    ^ @ o p q r s t u v ' w x y z A B C D 0 . ^     ",
"    ^ . ^ ^ ^ ^ . E ^ ^ . ^ . E ^ . ^ ^ ^ . . ^     ",
"    ^ . . . . . . . . . # = > . . . . . . . . ^     ",
"    ^ . . . . . . . . ] F G 3 + . . . . . . . ^     ",
"    ^ . . . . . . . . ^ H I J 8 A . . . . . . ^     ",
"    ^ . . . . K = = = = x z L M N O . . . . . ^     ",
"    ^ . . . P Q R R R R S T U V V W X ] . . . ^     ",
"    ^ . . . ) Y G G Z V V `  .G  .J ..6 # . . ^     ",
"    ^ . . . ^ +.@.C #.M $.: ~ ~ %.e &.` *.^ . ^     ",
"    ^ . . . . . =.-.V M ;.>.S M S ,.'.V -.+ . ^     ",
"    ^ . . . @ ).!.V V R ~.#.V V V {.].M M ^.. ^     ",
"    ^ . ^ P /.V (.Y V N + _.V V V :.<.V M 3 . ^     ",
"    ^ . [.W M &.}.|.M J O z 1.(.2.w *.V M 3.. ^     ",
"    ^ + 4.V 5.3.E 6.J V R 7.<.8.9.* U V $.; . ^     ",
"    ^ ' 0.|.r . . > d V V !.a.a b.c.V ..1 E . ^     ",
"    ^ . E d.. . . . e.f.V V V V V V ..g.0 . . ^     ",
"      . . . . . . . . # % L h.$.h.b.i ~.. . .       ",
"        . . . . . . . . ] ] i.- j.d.E . . .         ",
"          ^ . . . . . . . . . . . . . . .           ",
"            E . . . . . . . . . . . . ^             ",
"                . . . . . . . . . . >               ",
"                  . . . . . . . ^                   ",
"                    ] . . . . E                     ",
"                        > >                         ",
"                                                    ",
"                                                    ",
"                                                    "};
'''

    def Initialize(self):
        import FreeCAD as App
        import FreeCADGui as Gui
        from bimp import BlenderImport, MakeMaterial
        import bpy
        Gui.addCommand('Blender_Import', BlenderImport())
        Gui.addCommand('Make_Material',  MakeMaterial())
        commands = ['Blender_Import', 'Make_Material']
        # Add commands to menu and toolbar
        self.appendToolbar("Blender WorkBench", commands)
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
