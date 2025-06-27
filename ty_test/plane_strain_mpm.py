from geotaichi import *

init(dim=3, device_memory_GB=4)

mpm = MPM()

mpm.set_configuration(domain=[1.04, 0.14, 0.5],
                      background_damping=0.05,
                      alphaPIC=0.00005,
                      mapping="USL",
                      shape_function="GIMP",
                      gravity=[0., 0., -9.8]
                      )

mpm.set_solver({
                    "Timestep":         1e-6,
                    "SimulationTime":   0.2,
                    "SaveInterval":     0.002,
                    "SavePath":         './ty_test/DiskTarget_3D'
               })

mpm.memory_allocate(memory={
                            "max_material_number":           2,
                            "max_particle_number":           300000,
                            "max_constraint_number":  {
                                                           "max_reflection_constraint":   80000,
                                                           "max_velocity_constraint":   25000
                                                      },
                            "verlet_distance_multiplier":  0.8
                        })

mpm.add_contact(contact_type="MPMContact", friction=0.28)

mpm.add_material(model="DruckerPrager",
                 material={ "MaterialID": 1, "Density": 600, "YoungModulus": 6.1e7, "PoissionRatio": 0.2, "Friction": 16, "Dilation": 3.0 })

mpm.add_material(model="LinearElastic",
                 material={ "MaterialID": 2, "Density": 7850, "YoungModulus": 1e10, "PoissionRatio": 0.3 })

mpm.add_element(element={ "ElementType": "R8N3D", "ElementSize": [0.01, 0.01, 0.01] })

sphere_center_py = ti.Vector([0.52, 0.07, 0.3123])
sphere_radius_py = 0.0223

mpm.add_region(region=[{
                          "Name": "soil_region",
                          "Type": "Rectangle",
                          "BoundingBoxPoint": [0.02, 0.02, 0.02],
                          "BoundingBoxSize": [1.0, 0.1, 0.27]
                      },
                      {
                          "Name": "sphere_region",
                          "Type": "Spheroid",
                          "BoundingBoxPoint": sphere_center_py - sphere_radius_py,
                          "BoundingBoxSize": [2 * sphere_radius_py, 2 * sphere_radius_py, 2 * sphere_radius_py]
                      }])

mpm.add_body(body={
                   "Template": [{
                                   "RegionName":         "soil_region",
                                   "nParticlesPerCell":  2,
                                   "BodyID":             0,
                                   "MaterialID":         1,
                                   "InitialVelocity":    ti.Vector([0, 0, 0]),
                                   "FixVelocity":        ["Free", "Free", "Free"]
                               },
                               {
                                   "RegionName":         "sphere_region",
                                   "nParticlesPerCell":  2,
                                   "BodyID":             1,
                                   "MaterialID":         2,
                                   "InitialVelocity":    ti.Vector([0., 0., -1.12]),
                                   "FixVelocity":        ["Free", "Free", "Free"]
                               }]
               })

mpm.add_boundary_condition(boundary=[{
                                        "BoundaryType":   "VelocityConstraint",
                                        "Velocity":       [0, 0, 0],
                                        "StartPoint":     [0, 0, 0],
                                        "EndPoint":       [1.02, 0.12, 0.02]
                                    },
                                    { "BoundaryType": "ReflectionConstraint", "Norm": [-1, 0., 0], "StartPoint": [0., 0., 0.], "EndPoint": [0.02, 0.14, 0.5] },
                                    { "BoundaryType": "ReflectionConstraint", "Norm": [1, 0., 0], "StartPoint": [1.02, 0, 0], "EndPoint": [1.04, 0.14, 0.5] },
                                    { "BoundaryType": "ReflectionConstraint", "Norm": [0, -1., 0], "StartPoint": [0., 0., 0.], "EndPoint": [1.04, 0.02, 0.5] },
                                    { "BoundaryType": "ReflectionConstraint", "Norm": [0, 1., 0], "StartPoint": [0, 0.12, 0], "EndPoint": [1.04, 0.14, 0.5] }])

mpm.select_save_data()
mpm.run()
mpm.postprocessing()