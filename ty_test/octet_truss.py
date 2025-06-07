from geotaichi import *

init(device_memory_GB=6)

mpm = MPM()

mpm.set_configuration( 
                      domain=ti.Vector([0.17, 0.37, 0.21]),
                      background_damping=0.01,
                      alphaPIC=0.01, 
                      mapping="USL", 
                      shape_function="GIMP",
                      gravity=ti.Vector([0., -9.8, 0.]))

mpm.set_solver({
                "Timestep":         1e-5,
                "SimulationTime":   0.4,
                "SaveInterval":     0.002,
                "SavePath":         "Truss"
               })
                      
mpm.memory_allocate(memory={
                                "max_material_number":           1,
                                "max_particle_number":           1559361,
                                "verlet_distance_multiplier":    1.,
                                "max_constraint_number":  {
                                                               "max_reflection_constraint":   121914,
                                                               "max_friction_constraint":   0,
                                                               "max_velocity_constraint":   0
                                                          }
                            })


mpm.add_material(model="LinearElastic",
                 material={
                               "MaterialID":           1,
                               "Density":              2650.,
                               "YoungModulus":         2e6,
                               "PossionRatio":         0.3
                 })

mpm.add_element(element={
                             "ElementType":               "R8N3D",
                             "ElementSize":               ti.Vector([0.0025, 0.0025, 0.0025])
                        })

mpm.add_body_from_file(body={
                                    "FileType": "OBJ",
                                    "Template":  {
                                                   "BodyID": 0,
                                                   "MaterialID": 1,
                                                   "ParticleFile": "./assets/truss.obj",
                                                   "nParticlesPerCell": 4,
                                                   "Offset": [20, 20, 20],
                                                   "ScaleFactor": 0.005
                                                  }
                   })
                   
mpm.add_boundary_condition(boundary=[
                                    {
                                        "BoundaryType":   "ReflectionConstraint",
                                        "Norm":       [0., -1., 0.],
                                        "StartPoint":     [0., 0.006, 0.],
                                        "EndPoint":       [0.17, 0.008, 0.21]
                                    },
                                    ])

mpm.select_save_data(grid=True)

mpm.run()

