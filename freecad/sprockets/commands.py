""" FreeCAD commands.
"""

import os

import FreeCADGui
import FreeCAD as App

from .ansi_sprocket import AnsiSprocket
from .hub_sprocket import HubSprocket

from freecad.sprockets import ICONPATH


class AnsiSprocketCommand():
    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "ansi_sprocket_icon.png"),
            "MenuText": "ANSI sprocket",
            "ToolTip": "Creates new ANSI sprocket"
        }

    def Activated(self):
        ansi_sprocket = App.ActiveDocument.addObject(
            "Part::FeaturePython", "ANSI Sprocket"
        )
        AnsiSprocket(ansi_sprocket)

        App.ActiveDocument.recompute()

    def IsActive(self):
        if App.ActiveDocument is None:
            return False
        else:
            return True


class HubSprocketCommand():
    def GetResources(self):
        return {
            "Pixmap": os.path.join(ICONPATH, "hub_sprocket_icon.png"),
            "MenuText": "Hub sprocket",
            "ToolTip": "Creates new hub sprocket"
        }

    def Activated(self):
        hub_sprocket = App.ActiveDocument.addObject(
            "Part::FeaturePython", "Hub Sprocket"
        )
        HubSprocket(hub_sprocket)

        App.ActiveDocument.recompute()

    def IsActive(self):
        if App.ActiveDocument is None:
            return False
        else:
            return True
