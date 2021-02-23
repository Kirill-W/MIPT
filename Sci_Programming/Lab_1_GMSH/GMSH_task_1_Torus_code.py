import gmsh
import sys
import math

gmsh.initialize(sys.argv)
gmsh.model.add("torus_cut")

torus1 = gmsh.model.occ.addTorus(0, 0, 0, 0.5, 0.2, 1, 2*math.pi)
gmsh.model.occ.addPlaneSurface([1], 4)

torus2 = gmsh.model.occ.addTorus(0, 0, 0, 0.5, 0.1, 2, 2*math.pi)
gmsh.model.occ.addPlaneSurface([2], 8)

gmsh.model.occ.cut([(3, 1)], [(3, 2)], 3)

gmsh.model.occ.mesh.setSize(gmsh.model.occ.getEntities(), 0.025)

gmsh.model.occ.synchronize()
gmsh.model.mesh.generate()
gmsh.write("Torus.vtk")

gmsh.finalize()
