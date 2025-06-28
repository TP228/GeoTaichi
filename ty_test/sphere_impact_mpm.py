from geotaichi import *

init(dim=3, arch='cpu')

mpm = MPM()

mpm.set_configuration(domain=[10., 6., 5.],
                      background_damping=0., 
                      alphaPIC=0.005, 
                      mapping="USF", 
                      shape_function="GIMP",
                      gravity=[0., 0., 0.])

mpm.set_solver({
                      "Timestep":         1e-5,
                      "SimulationTime":   0.1,
                      "SaveInterval":     1e-3,
                      "SavePath":         './ty_test/DiskDisk'
                 })

mpm.memory_allocate(memory={
                                "max_material_number":           1,
                                "max_particle_number":           80000,
                                "max_constraint_number":  {
                                                               "max_reflection_constraint":   61820
                                                          }
                            })

mpm.add_contact(contact_type="MPMContact", friction=0.5)

mpm.add_material(model="LinearElastic",
                 material={
                               "MaterialID":           1,
                               "Density":              2650.,
                               "YoungModulus":         1e10,
                               "PoissionRatio":        0.3
                 })

mpm.add_element(element={
                             "ElementType":               "R8N3D",
                             "ElementSize":               [0.1, 0.1, 0.1]
                        })

sphere1_center_py = ti.Vector([4.4, 3.0, 3.0])
sphere1_radius_py = 0.5
sphere2_center_py = ti.Vector([5.6, 3.0, 3.0])
sphere2_radius_py = 0.5

mpm.add_region(region=[{
                            "Name": "sphere1_region",
                            "Type": "Spheroid",
                            "BoundingBoxPoint": sphere1_center_py - sphere1_radius_py,
                            "BoundingBoxSize": [2 * sphere1_radius_py, 2 * sphere1_radius_py, 2 * sphere1_radius_py]
                      },
                      {
                            "Name": "sphere2_region",
                            "Type": "Spheroid",
                            "BoundingBoxPoint": sphere2_center_py - sphere2_radius_py,
                            "BoundingBoxSize": [2 * sphere2_radius_py, 2 * sphere2_radius_py, 2 * sphere2_radius_py]
                      }])

mpm.add_body(body={
                       "Template": [{
                                       "RegionName":         "sphere1_region",
                                       "nParticlesPerCell":  4,
                                       "BodyID":             0,
                                       "MaterialID":         1,
                                       "InitialVelocity":    ti.Vector([2., 0., 0.])
                                   },
                                   {
                                       "RegionName":         "sphere2_region",
                                       "nParticlesPerCell":  4,
                                       "BodyID":             1,
                                       "MaterialID":         1,
                                       "InitialVelocity":    ti.Vector([-2., 0., 0.])
                                   }]
                   })

mpm.add_boundary_condition(boundary=[{
                                        "BoundaryType":   "ReflectionConstraint",
                                        "Norm":           [0., 0., -1],
                                        "StartPoint":     [0., 0., 0.],
                                        "EndPoint":       [10., 6., 0.]
                                    },
                                    { "BoundaryType": "ReflectionConstraint", "Norm": [-1, 0., 0], "StartPoint": [0., 0., 0.], "EndPoint": [0., 6., 5.] },
                                    { "BoundaryType": "ReflectionConstraint", "Norm": [1, 0., 0], "StartPoint": [10., 0., 0.], "EndPoint": [10., 6., 5.] },
                                    { "BoundaryType": "ReflectionConstraint", "Norm": [0, -1., 0], "StartPoint": [0., 0., 0.], "EndPoint": [10., 0., 5.] },
                                    { "BoundaryType": "ReflectionConstraint", "Norm": [0, 1., 0], "StartPoint": [0., 6., 0.], "EndPoint": [10., 6., 5.] }])

mpm.select_save_data()
mpm.run()
mpm.postprocessing()