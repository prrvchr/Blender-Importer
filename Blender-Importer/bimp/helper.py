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

""" FreeCAD Helper """

import FreeCAD as App

from PySide2.QtWidgets import QFileDialog

import os
import bpy
import json
import mathutils

from ArchMaterial import makeMaterial


def importFile(doc):
    warnings = []
    root = 'Blender'
    maxpolygons = 1000
    path, fname = os.path.split(doc.FileName)
    filename, ext = os.path.splitext(fname)
    App.Console.PrintMessage(f"Activated active document name: {filename}\n")

    # get and open the Blender file
    path = App.ParamGet('User parameter:BaseApp/Preferences/General').GetString('FileOpenSavePath')
    url, filter = QFileDialog.getOpenFileName(None, 'Import Blender file', path, 'Blender file (*.blend)')
    if not url:
        App.Console.PrintMessage("\n")
        App.Console.PrintMessage("No file as been chosen, can't continue...\n")
        return False, warnings, url
    bpy.ops.wm.open_mainfile(filepath=url)

    # get the Blender collection having same name as the .blend file name (without extension)
    bcoll = bpy.data.collections.get(filename)
    if bcoll is None:
        App.Console.PrintMessage("\n")
        App.Console.PrintMessage(f"No collection named: {filename}, can't continue... ")
        collections = []
        for bcoll in bpy.data.collections:
            collections.append(bcoll.name)
        App.Console.PrintMessage(f"Available collections: {', '.join(collections)}\n")
        return False, warnings, url

    # get a dict of FreeCAD materials in the document
    materials = {obj.Label: obj for obj in doc.Objects if isValidMaterial(obj)}

    # browse all materiels in the Blender scene
    for bmat in bpy.data.materials:
        if not bmat.use_nodes:
            msg = f"Blender material: {bmat.name}, don't use node, skipped...\n"
            warnings.append(msg)
            App.Console.PrintMessage(msg)
            continue
        if bmat.name in materials and materials[bmat.name].Material.get(root):
            msg = f"FreeCAD material: {bmat.name}, already has a Blender configuration, skipped...\n"
            warnings.append(msg)
            App.Console.PrintMessage(msg)
            continue

        matdata = {}
        for node in bmat.node_tree.nodes:
            links = {}
            inputs = {}
            outputs = {}
            sockets = {}

            if node.inputs:
                link, input = _getInputData(warnings, bmat, node)
                links.update(link)
                inputs.update(input)

            if node.outputs:
                output = _getOutputs(warnings, bmat, node)
                outputs.update(output)

            sockets = _getSocketProperties(warnings, node, bmat.name, node.name, [])

            matdata[node.name] = {'Type':     node.__class__.__name__,
                                  'Sockets':  sockets,
                                  'Link':     links,
                                  'Inputs':   inputs,
                                  'Outputs':  outputs}

        if matdata:
            if bmat.name in materials:
                mat = materials[bmat.name]
            else:
                mat = makeMaterial(bmat.name)
                materials[bmat.name] = mat
            temp = mat.Material.copy()
            temp[root] = json.dumps(tuple(matdata.keys()))
            for node, data in matdata.items():
                temp[root + '.' + node] = json.dumps(data)
            mat.Material = temp

    # get a dict of FreeCAD objects (label -> name) in the document
    objects = {obj.Label: obj.Name for obj in doc.Objects if obj.Label not in materials.keys()}

    # browse all objects in the Blender collection
    for bobj in bcoll.objects:
        name = objects.get(bobj.name)
        if name is None:
            msg = f"Blender object: {bobj.name} does not have a corresponding FreeCAD object, skipped...\n"
            warnings.append(msg)
            App.Console.PrintMessage(msg)
            continue
        obj = doc.getObject(name)
        if obj is None:
            msg = f"FreeCAD object: {name} with Label: {bobj.name}, can't be retrieved, skipped...\n"
            warnings.append(msg)
            App.Console.PrintMessage(msg)
            continue

        # create material if not exist
        bmat = bobj.active_material
        if bmat:
            if bmat.name not in materials:
                transparency = round(alpha * 100)
                mat = makeMaterial(bmat.name, (r, g, b), transparency)
                materials[bmat.name] = mat
                msg = f"FreeCAD object: {name} appears to have material: {bmat.name} that is not listed!!!\n"
                warnings.append(msg)
                App.Console.PrintMessage(msg)
            else:
                mat = materials[bmat.name]
            if 'Material' not in obj.PropertiesList:
                obj.addProperty('App::PropertyLink', 'Material')
            obj.Material = mat

        # set material all faces
        fmat = {}
        bfaces = bobj.data.polygons
        if bfaces and len(bfaces) < maxpolygons:
            bindex = bobj.active_material_index
            for bface in bfaces:
                if bface.material_index != bindex:
                    bslot = bobj.material_slots[bface.material_index]
                    if bslot is None or not bslot.material:
                        continue
                    App.Console.PrintMessage(f"object: {bobj.name} - face: {bface.index} - materiel_index: {bface.material_index}\n")
                    if bslot.material.name not in fmat:
                        fmat[bslot.material.name] = []
                    fmat[bslot.material.name].append(bface.index)
            if fmat:
                if 'MaterialFaces' not in obj.PropertiesList:
                    obj.addProperty('App::PropertyString', 'MaterialFaces')
                data = json.dumps(fmat)
                obj.MaterialFaces = data
                App.Console.PrintMessage(f"object: {bobj.name} - faces materials: {data}\n")
        if not fmat and 'MaterialFaces' in obj.PropertiesList:
            obj.removeProperty('MaterialFaces')

    return True, warnings, url

def isMultiMaterial(obj):
    """Check if a material is a multimaterial."""
    try:
        feature = obj.isDerivedFrom('App::FeaturePython')
    except AttributeError:
        return False

    multimat = _getproxyattr(obj, 'Type') == 'MultiMaterial'

    return obj is not None and feature and multimat

def isValidMaterial(obj):
    """Assert that an object is a valid Material."""
    try:
        is_materialobject = obj.isDerivedFrom('App::MaterialObjectPython')
    except AttributeError:
        return False

    return (obj is not None and
            is_materialobject and
            hasattr(obj, 'Material') and
            isinstance(obj.Material, dict))


# Private function

def _getInputData(warnings, bmat, node):
    links = {}
    inputs = {}
    for input in node.inputs:
        for link in input.links:
            links[input.name] = (link.from_node.name, link.from_socket.name)
        if input.type == 'VALUE':
            v = input.default_value
            value = v
        elif input.type == 'VECTOR':
            v = input.default_value
            value = (v[0], v[1], v[2])
        elif input.type == 'RGBA':
            v = input.default_value
            value = (v[0], v[1], v[2], v[3])
        elif input.type == 'SHADER':
            continue
        else:
            msg = f"FreeCAD material {bmat.name} on node {node.name} can't read input: {input.name} type {input.type} is not supported, skipping...\n"
            warnings.append(msg)
            App.Console.PrintMessage(msg)
            continue
        App.Console.PrintMessage(f"Material Name: {bmat.name} Node: {node.name} Input: {input.name} - Value: {value}\n")
        inputs[input.name] = value
    return links, inputs

def _getOutputs(warnings, bmat, node):
    outputs = {}
    for output in node.outputs:
        if output.type == 'VALUE':
            v = output.default_value
            value = v
        elif output.type == 'VECTOR':
            v = output.default_value
            value = (v[0], v[1], v[2])
        elif output.type == 'RGBA':
            v = output.default_value
            value = (v[0], v[1], v[2], v[3])
        elif output.type == 'SHADER':
            continue
        else:
            msg = f"FreeCAD material {bmat.name} on node {node.name} can't read output: {output.name} type {output.type} is not supported, skipping...\n"
            warnings.append(msg)
            App.Console.PrintMessage(msg)
            continue
        App.Console.PrintMessage(f"Material Name: {bmat.name} Node: {node.name} output: {output.name} - Value: {value}\n")
        outputs[output.name] = value
    return outputs

def _getSocketProperties(warnings, obj, mat, node, properties):
    data = {}
    skipping = ('rna_type', 'inputs', 'outputs', 'dimensions', 'type',
                'is_hidden', 'from_node', 'from_socket', 'to_node', 'to_socket')
    for p in dir(obj):
        if p not in skipping and not (p.startswith('_') or p.startswith('bl_')):
            v = getattr(obj, p)
            if v is None or isinstance(v, bpy.types.bpy_func):
                continue
            elif isinstance(v, (str, int, float, bool)):
                value = v
            elif isinstance(v, mathutils.Color):
                value = {'r': v.r, 'g': v.g, 'b': v.b}
            elif isinstance(v, mathutils.Euler):
                value = {'x': v.x, 'y': v.y, 'z': v.z, 'order': v.order}
            elif isinstance(v, mathutils.Vector):
                if len(v) == 2:
                    value = {'x': v.x, 'y': v.y}
                elif len(v) == 3:
                    value = {'x': v.x, 'y': v.y, 'z': v.z}
                elif len(v) == 4:
                    value = {'x': v.x, 'y': v.y, 'z': v.z, 'w': v.w}
            elif isinstance(v, bpy.types.bpy_prop_array):
                value = []
                for d in v:
                    value.append(d)
            elif isinstance(v, bpy.types.bpy_prop_collection):
                value = {}
                properties.append(p)
                for k, d in v.items():
                    value[k] = _getSocketProperties(warnings, d, mat, node, properties)
            elif isinstance(v, bpy.types.TexMapping):
                properties.append(p)
                value = _getSocketProperties(warnings, v, mat, node, properties)
            elif isinstance(v, bpy.types.ColorRamp):
                properties.append(p)
                value = _getSocketProperties(warnings, v, mat, node, properties)
            elif isinstance(v, bpy.types.ColorMapping):
                properties.append(p)
                value = _getSocketProperties(warnings, v, mat, node, properties)
            else:
                msg = f"FreeCAD material {mat} on node {node} can't read property: {p} type {type(v)} is not supported, skipping...\n"
                warnings.append(msg)
                App.Console.PrintMessage(msg)
                continue
            data[p] = value
            properties.append(p)
            App.Console.PrintMessage(f"Node socket: {node} property: {'.'.join(properties)} value: {str(value)}\n")
    return data

def _getproxyattr(obj, name, default=None):
    """Get attribute on object's proxy."""

    # Behaves like getattr, but on Proxy property, and with mandatory default...

    try:
        res = getattr(obj.Proxy, name, default)
    except AttributeError:
        res = default
    return res
