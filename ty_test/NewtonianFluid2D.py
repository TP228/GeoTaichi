from geotaichi import *

import numpy as np

total_time = 20.
dt = 1e-6
t_arr = np.arange(0, total_time, dt)

g = 9.81
A = np.deg2rad(5)
omega = 2 * np.pi / (6.61 / 1)

theta_t = A * np.sin(omega * t_arr)

bx_t = -g * np.sin(theta_t)
by_t = -g * np.cos(theta_t)

gravity_table = np.stack([bx_t, by_t], axis=1)  # shape = (num_time_steps, 2)

init(dim=2, device_memory_GB=3.7)

mpm = MPM()

mpm.set_configuration(domain=[1., 1.],
                      background_damping=0.0,
                      alphaPIC=1.0, 
                      mapping="USL", 
                      shape_function="Linear",
                      gravity=gravity_table,
                    #   gravity=[0., -9.8],
                      material_type="Fluid",
                      velocity_projection="Affine") #"also support for Taylor PIC"

mpm.set_solver({
                      "Timestep":         dt,
                      "SimulationTime":   20,
                      "SaveInterval":     1e-3,
                      "SavePath":         './Sloshing'
                 }) 
                      
mpm.memory_allocate(memory={
                                "max_material_number":           1,
                                "max_particle_number":           56000,
                                "verlet_distance_multiplier":    1.,
                                "max_constraint_number":  {
                                                               "max_reflection_constraint":   541681
                                                          }
                            })
                            
mpm.add_material(model="Newtonian",
                 material={
                               "MaterialID":           1,
                               "Density":              1000.,
                               "Modulus":              2e6,
                               "Viscosity":            1.01e-3,
                               "ElementLength":        0.02,
                               "cL":                   1.0,
                               "cQ":                   2
                 })

mpm.add_element(element={
                             "ElementType":               "Q4N2D",
                             "ElementSize":               [0.02, 0.02]
                        })


mpm.add_region(region=[{
                            "Name": "region1",
                            "Type": "Rectangle2D",
                            "BoundingBoxPoint": [0.0, 0.0],
                            "BoundingBoxSize": [1., 0.3],
                            "ydirection": [0., 1.]
                      }])

mpm.add_body(body={
                       "Template": [{
                                       "RegionName":         "region1",
                                       "nParticlesPerCell":  4,
                                       "BodyID":             0,
                                       "MaterialID":         1,
                                       "ParticleStress": {
                                                              "GravityField":     True,
                                                              "InternalStress":   ti.Vector([-0., -0., -0., 0., 0., 0.])
                                                         },
                                       "InitialVelocity":[0, 0, 0],
                                       "FixVelocity":    ["Free", "Free", "Free"]    
                                       
                                   }]
                   })
                   

mpm.add_boundary_condition(boundary=[
                                    {
                                        "BoundaryType":   "ReflectionConstraint",
                                        "Norm":       [-1., 0.],
                                        "StartPoint":     [0, 0],
                                        "EndPoint":       [0., 1.],
                                    },
                                    
                                    {
                                        "BoundaryType":   "ReflectionConstraint",
                                        "Norm":       [1., 0.],
                                        "StartPoint":     [1., 0],
                                        "EndPoint":       [1., 1.],
                                    },
                                    
                                    {
                                        "BoundaryType":   "ReflectionConstraint",
                                        "Norm":       [0., -1.],
                                        "StartPoint":     [0, 0],
                                        "EndPoint":       [1., 0.],
                                    },
                                    
                                    {
                                        "BoundaryType":   "ReflectionConstraint",
                                        "Norm":       [0., 1.],
                                        "StartPoint":     [0, 1.],
                                        "EndPoint":       [1., 1.],
                                    }])


mpm.select_save_data(grid=True)

mpm.run()

mpm.postprocessing()


