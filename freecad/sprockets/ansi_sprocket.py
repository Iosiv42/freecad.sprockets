""" Parametric object for ANSI sprockets.
Sources: http://www.gearseds.com/files/design_draw_sprocket_5.pdf,
         https://www.chiefdelphi.com/t/sprocket-design-tutorial/387449
"""

import math


class AnsiSprocket:
    def __init__(self, obj):
        """ Modify object to add necessary properties. """

        for obj_property in (
            ("ChainPitch", "Pitch of chain"),
            ("RollerDiameter", "Diameter of chain roller"),
            ("Thickness", "Thickness of sprocket"),
        ):
            obj.addProperty(
                "App::PropertyLength", obj_property[0], "Base", obj_property[1]
            )

        obj.addProperty(
            "App::PropertyLength", "ChamferWidth", "Misc",
            "Width of chamfer. (Can cause recompute slowing down)"
        )
        obj.addProperty(
            "App::PropertyLength", "ChamferHeight", "Misc",
            "Height of chamfer. (Can cause recompute slowing down)"
        )
        obj.addProperty(
            "App::PropertyLength", "TeethCut", "Misc",
            "Length of teeth cut. I.e. resulting shape is common of "
            "sprocket and cylinder with radius = (outer radius - teeth cut) "
            "and thickness = sprocket thickness. "
            "(Can cause recompute slowing down)"
        )

        obj.addProperty(
            "App::PropertyInteger", "TeethAmount", "Base", "Teeth amount"
        )
        
        obj.Proxy = self
        obj.ViewObject.Proxy = 0

        obj.ChainPitch = 12.7
        obj.RollerDiameter = 7.62
        obj.TeethAmount = 32
        obj.Thickness = 4

        obj.ChamferWidth = 0
        obj.ChamferHeight = 0
        obj.TeethCut = 0

        obj.Label = "ANSI Sprocket"

    def execute(self, obj):
        """ Update object when values changed. """

        # Cf. sources at top of file for explanations of calculations.

        import math
        cos = math.cos
        sin = math.sin

        import FreeCAD
        import Part
        import Draft

        Units = FreeCAD.Units

        # Angular diameter of half tooth.
        segment_angle = math.pi / obj.TeethAmount

        # Length from center of sprocket to center of chain roller.
        pitch_diameter = obj.ChainPitch / sin(segment_angle)

        seating_diameter = 1.005*obj.RollerDiameter
        seating_diameter -= Units.Quantity(0.0762, Units.Length)

        # Auxiliary values.
        a = 35 + 60/obj.TeethAmount
        b = 18 - 56/obj.TeethAmount
        ac = 0.8 * obj.RollerDiameter
        ab = 1.4 * obj.RollerDiameter
        r1 = seating_diameter/2

        seating_arc = Part.makeCircle(
            r1,
            FreeCAD.Vector(0, pitch_diameter/2, 0),
            FreeCAD.Vector(0, 0, 1),
            a - 180, -a
        )

        xy_arc = Part.makeCircle(
            r1 + ac,
            FreeCAD.Vector(
                ac*cos(math.radians(a)),
                ac*sin(math.radians(a)) + pitch_diameter/2,
                0
            ),
            FreeCAD.Vector(0, 0, 1),
            a - b - 180, a - 180
        )

        zn_arc_center = FreeCAD.Vector(
            -ab*cos(segment_angle), pitch_diameter/2 - ab*sin(segment_angle)
        )

        k = (
            xy_arc.Vertexes[0].X * (1 / math.tan(math.radians(a - b)))
            + xy_arc.Vertexes[0].Y
        )
        zn_arc_radius = abs(
            zn_arc_center.x*cos(math.radians(a - b))
            + (zn_arc_center.y - k) * sin(math.radians(a - b))
        )

        zn_arc = Part.makeCircle(
            zn_arc_radius, zn_arc_center, FreeCAD.Vector(0, 0, 1),
            a - b, math.degrees(segment_angle + math.acos(
                cos(
                    -segment_angle - math.atan2(zn_arc_center.y, -zn_arc_center.x)
                ) * zn_arc_center.Length / zn_arc_radius
            ))
        )

        yz_line = Part.makeLine(
            xy_arc.Vertexes[0].Point, zn_arc.Vertexes[0].Point
        )

        mirror_line = (FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0))
        shapes = (
            zn_arc.mirror(*mirror_line),
            yz_line.mirror(*mirror_line),
            xy_arc.mirror(*mirror_line),
            seating_arc,
            xy_arc,
            yz_line,
            zn_arc
        )

        # Go round to enclose sprocket wire.
        tooth_wire = Part.Wire(shapes)
        wires = []
        for n in range(obj.TeethAmount):
            wires.append(tooth_wire.rotate(
                FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 0, 1),
                math.degrees(2*segment_angle)
            ).copy())

        sprocket_face = Part.Face(Part.Wire(wires))
        sprocket = sprocket_face.extrude(FreeCAD.Vector(0, 0, obj.Thickness))

        if (obj.TeethCut != 0
            or obj.ChamferWidth != 0
            or obj.ChamferHeight != 0
        ):
            # Apply misc. parameters if necessary.
            outer_radius = Units.Quantity(
                zn_arc.Vertexes[1].Point.Length, Units.Length
            )

            pig = Part.makeCylinder(outer_radius - obj.TeethCut, obj.Thickness)

            if obj.ChamferWidth != 0 and obj.ChamferHeight != 0:
                pig = pig.makeChamfer(
                    obj.ChamferWidth, obj.ChamferHeight, pig.Edges[::2]
                )

            sprocket = pig.common(sprocket)

        obj.Shape = sprocket
