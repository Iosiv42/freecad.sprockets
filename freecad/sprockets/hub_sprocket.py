""" Hub sprocket parametric object.
Sources: https://www.chiefdelphi.com/t/sprocket-design-tutorial/387449
"""

class HubSprocket:
    def __init__(self, obj):
        """ Modify object to add necessary properties. """

        for property_name in ("ChainPitch", "RollerDiameter", "Thickness"):
            obj.addProperty("App::PropertyLength", property_name)

        obj.addProperty("App::PropertyInteger", "TeethAmount")
        
        obj.Proxy = self
        obj.ViewObject.Proxy = 0
        obj.ChainPitch = 12.7
        obj.RollerDiameter = 7.62
        obj.TeethAmount = 32
        obj.Thickness = 4
        obj.Label = "Hub Sprocket"

    def execute(self, obj):
        """ Update object when values changed. """

        # Cf. sources at top of file for explanations of calculations.

        import math

        import FreeCAD
        import Part
        import Draft

        # Angular diameter of half tooth.
        segment_angle = math.pi / obj.TeethAmount

        # Length from center of sprocket to center of chain roller.
        pitch_diameter = obj.ChainPitch / math.sin(segment_angle)

        roller_arc = Part.makeCircle(
            obj.RollerDiameter/2,
            FreeCAD.Vector(0, pitch_diameter/2, 0),
            FreeCAD.Vector(0, 0, 1),
            math.degrees(segment_angle - math.pi),
            math.degrees(-segment_angle)
        )

        secondary_arc = Part.makeCircle(
            obj.ChainPitch - obj.RollerDiameter/2,
            FreeCAD.Vector(
                -pitch_diameter/2 * math.sin(2*segment_angle),
                pitch_diameter/2 * math.cos(2*segment_angle),
                0
            ),
            FreeCAD.Vector(0, 0, 1),
            math.degrees(segment_angle),
            math.degrees(
                math.acos(
                    obj.ChainPitch / (2*obj.ChainPitch - obj.RollerDiameter)
                ) + segment_angle
            )
        )

        outer_radius = (
            float(obj.ChainPitch) * (1/math.tan(segment_angle))/2
            + math.sqrt(
                (obj.ChainPitch - obj.RollerDiameter/2)**2
                - obj.ChainPitch**2 / 4
            )
        )

        arcs = (
            secondary_arc.mirror(
                FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0)
            ),
            roller_arc,
            secondary_arc,
        )

        # Go round to enclose sprocket wire.
        tooth_wire = Part.Wire(arcs)
        wires = []
        for n in range(obj.TeethAmount):
            wires.append(tooth_wire.rotate(
                FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1),
                math.degrees(2*segment_angle)
            ).copy())

        sprocket_face = Part.Face(Part.Wire(wires))
        sprocket = sprocket_face.extrude(FreeCAD.Vector(0, 0, obj.Thickness))

        obj.Shape = sprocket
