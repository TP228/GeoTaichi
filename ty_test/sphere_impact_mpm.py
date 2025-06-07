from geotaichi import *

init(arch='cpu')

mpm = MPM()

mpm.set_configuration(domain=ti.Vector([10., 6., 5.]),
                      background_damping=0., 
                      alphaPIC=0.005, 
                      mapping="USF", 
                      shape_function="Linear",
                      gravity=ti.Vector([0., 0., 0.]),
                      velocity_projection="Affine")

mpm.set_solver({
                      "Timestep":         1e-6,
                      "SimulationTime":   0.1,
                      "SaveInterval":     1e-3,
                      "SavePath":         './DiskDisk'
                 })    
     
mpm.memory_allocate(memory={
                                "max_material_number":           1,
                                "max_particle_number":           56000,
                                "verlet_distance_multiplier":    1.,
                                "max_constraint_number":  {
                                                               "max_reflection_constraint":   541681
                                                          }
                            })

mpm.add_contact(contact_type="MPMContact")

mpm.add_material(model="LinearElastic",
                 material={
                               "MaterialID":           1,
                               "Density":              2650.,
                               "YoungModulus":         1e10,
                               "PoissionRatio":        0.3
                 })

mpm.add_element(element={
                             "ElementType":               "R8N3D",
                             "ElementSize":               ti.Vector([0.1, 0.1, 0.1]),
                             "Contact":                   {
                                                               "ContactDetection":                True
                                                          } 
                        })

mpm.add_region(region=[{
                            "Name": "region1",
                            "Type": "Spheroid",
                            "BoundingBoxPoint": ti.Vector([5.1, 2.5, 2.5]),
                            "BoundingBoxSize": ti.Vector([0.25, 0.25, 0.25]),
                            "zdirection": ti.Vector([0., 0., 1.])
                      },
                      
                      {
                            "Name": "region2",
                            "Type": "Spheroid",
                            "BoundingBoxPoint": ti.Vector([4.4, 3.0, 3.0]),
                            "BoundingBoxSize": ti.Vector([0.25, 0.25, 0.25]),
                            "zdirection": ti.Vector([0., 0., 1.])
                      }])

mpm.add_body(body={
                       "Template": [{
                                       "RegionName":         "region1",
                                       "nParticlesPerCell":  4,
                                       "BodyID":             0,
                                       "MaterialID":         1,
                                       "ParticleStress": {
                                                              "GravityField":     False,
                                                              "InternalStress":   ti.Vector([-0., -0., -0., 0., 0., 0.])
                                                         },
                                       "InitialVelocity":ti.Vector([-1, 0, 0]),
                                       "FixVelocity":    ["Free", "Free", "Free"]    
                                       
                                   },
                                   
                                   {
                                       "RegionName":         "region2",
                                       "nParticlesPerCell":  4,
                                       "BodyID":             1,
                                       "MaterialID":         1,
                                       "ParticleStress": {
                                                              "GravityField":     False,
                                                              "InternalStress":   ti.Vector([-0., -0., -0., 0., 0., 0.])
                                                         },
                                       "InitialVelocity":ti.Vector([1, 0, 0]),
                                       "FixVelocity":    ["Free", "Free", "Free"]    
                                       
                                   }]
                   })

mpm.add_boundary_condition(boundary=[{
                                        "BoundaryType":   "ReflectionConstraint",
                                        "Norm":           [0., 0., -1],
                                        "StartPoint":     [0., 0., 0.],
                                        "EndPoint":       [10., 6., 0.]
                                    },
                                    
                                    {
                                        "BoundaryType":   "ReflectionConstraint",
                                        "Norm":           [-1, 0., 0],
                                        "StartPoint":     [0., 0., 0.],
                                        "EndPoint":       [0., 2., 0.]
                                    },
                                    
                                    {
                                        "BoundaryType":   "ReflectionConstraint",
                                        "Norm":           [1, 0., 0],
                                        "StartPoint":     [6., 0., 0.],
                                        "EndPoint":       [6., 2., 0.]
                                    },
                                    
                                    {
                                        "BoundaryType":   "ReflectionConstraint",
                                        "Norm":           [0, -1., 0],
                                        "StartPoint":     [0., 0., 0.],
                                        "EndPoint":       [6., 0., 0.]
                                    },
                                    
                                    {
                                        "BoundaryType":   "ReflectionConstraint",
                                        "Norm":           [0, 1., 0],
                                        "StartPoint":     [0., 2., 0.],
                                        "EndPoint":       [6., 2., 0.]
                                    }])

mpm.select_save_data(grid=True)

mpm.run()

mpm.postprocessing()
