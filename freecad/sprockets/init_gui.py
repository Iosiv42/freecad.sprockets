import os
import FreeCAD
import FreeCADGui as Gui

from freecad.sprockets import ICONPATH


class SprocketsWorkbench(Gui.Workbench):
    MenuText = "Sprockets"
    ToolTip = "Workbench for creating sprockets"
    Icon = os.path.join(ICONPATH, "workbench_icon.svg")

    def Initialize(self):
        """This function is executed when the workbench is first activated.
        
        It is executed once in a FreeCAD session followed by the Activated function.
        """

        from .commands import HubSprocketCommand, AnsiSprocketCommand

        self.commands = ["AnsiSprocket", "HubSprocket"]
        self.appendToolbar("Commands", self.commands)

        Gui.addCommand("HubSprocket", HubSprocketCommand())
        Gui.addCommand("AnsiSprocket", AnsiSprocketCommand())

    def Activated(self):
        """This function is executed whenever the workbench is activated"""
        return

    def Deactivated(self):
        """This function is executed whenever the workbench is deactivated"""
        return

    def ContextMenu(self, recipient):
        """This function is executed whenever the user right-clicks on screen"""

        self.appendContextMenu("Commands", self.list)

    def GetClassName(self): 
        return "Gui::PythonWorkbench"
       
Gui.addWorkbench(SprocketsWorkbench())
