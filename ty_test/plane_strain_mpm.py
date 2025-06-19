# coding=utf-8
from geotaichi import *

# 1. 시뮬레이션 초기화
init(dim=3, device_memory_GB=4.0)

# 2. MPM 솔버 객체 생성
# 기존 DEMPM() 대신 MPM()을 사용
mpm = MPM()

# 3. MPM 솔버 환경설정
# 기존 mpm 설정과 동일한 파라미터 적용
mpm.set_configuration(
                        background_damping=0.05,
                        alphaPIC=0.00005,
                        mapping="USL",
                        shape_function="GIMP",
                        gravity=ti.Vector([0., 0., -9.8]))

# 4. 시뮬레이션 시간 및 저장 설정
mpm.set_solver({
                    "Timestep":         1e-6,
                    "SimulationTime":   0.2,
                    "SaveInterval":     0.002,
                    "SavePath":         './DiskTarget' # 결과 저장 경로 변경
                })

# 5. 메모리 할당
# Material 2개(낙하 구, 지반), Particle 수는 충분히 할당
mpm.memory_allocate(memory={
                            "max_material_number":           2,
                            "max_particle_number":           300000,
                            "max_constraint_number":  {
                                                            "max_reflection_constraint":   61820,
                                                            "max_velocity_constraint":   12501
                                                        },
                            "verlet_distance_multiplier":  0.8
                        })

# 6. 재료(Material) 정의
# MaterialID 0: 낙하 구 (강철과 유사한 물성의 선형 탄성체로 모델링)
mpm.add_material(model="LinearElastic",
                 material={
                               "MaterialID":                    0,
                               "Density":                       7850.0,
                               "YoungModulus":                  2.1e11, # 강성을 높게 설정
                               "PoissionRatio":                 0.3,
                 })

# MaterialID 1: 지반 (기존 Drucker-Prager 물성치와 동일)
mpm.add_material(model="DruckerPrager",
                 material={
                               "MaterialID":                    1,
                               "Density":                       600.0,
                               "YoungModulus":                  6.1e7,
                               "PoissionRatio":                 0.2,
                               "Friction":                      16,
                               "Dilation":                      3.0,
                               "Cohesion":                      0.0,
                               "Tensile":                       0.0
                 })

# 7. 요소(Element) 정의
mpm.add_element(element={
                             "ElementType":               "R8N3D",
                             "ElementSize":               ti.Vector([0.01, 0.01, 0.01])
                        })

# 8. 객체 생성을 위한 영역(Region) 정의
mpm.add_region(region=[{
                            # Region 'ground': 지반 영역
                            "Name": "ground",
                            "Type": "Rectangle",
                            "BoundingBoxPoint": ti.Vector([0.02, 0.02, 0.02]),
                            "BoundingBoxSize": ti.Vector([1.0, 0.1, 0.27])
                      },
                      {
                            # Region 'impactor': 낙하 구 영역
                            "Name": "impactor",
                            "Type": "Sphere",
                            "Center": ti.Vector([0.52, 0.07, 0.3123]), # 기존 DEM 구의 위치
                            "Radius": 0.0223                          # 기존 DEM 구의 반경
                      }])

# 9. 영역에 입자(Body) 생성
mpm.add_body(body={
                       "Template": [{
                                       "RegionName":         "ground",
                                       "nParticlesPerCell":  2,
                                       "MaterialID":         1, # 지반 Material
                                       "InitialVelocity":    ti.Vector([0, 0, 0])
                                   },
                                   {
                                       "RegionName":         "impactor",
                                       "nParticlesPerCell":  2,
                                       "MaterialID":         0, # 낙하 구 Material
                                       "InitialVelocity":    ti.Vector([0., 0., -1.12]) # 기존 DEM 구의 초기 속도
                                   }]
                   })

# 10. 경계 조건(Boundary Condition) 설정
# 기존과 동일한 도메인 경계 조건 적용
mpm.add_boundary_condition(boundary=[{
                                        "BoundaryType":   "VelocityConstraint",
                                        "Velocity":       [0, 0, 0],
                                        "StartPoint":     [0, 0, 0],
                                        "EndPoint":       [1.02, 0.12, 0.02]
                                    },
                                    {
                                        "BoundaryType":   "ReflectionConstraint",
                                        "Norm":           [-1, 0., 0],
                                        "StartPoint":     [0., 0., 0.],
                                        "EndPoint":       [0.02, 0.14, 0.5]
                                    },
                                    {
                                        "BoundaryType":   "ReflectionConstraint",
                                        "Norm":           [1, 0., 0],
                                        "StartPoint":     [1.02, 0, 0],
                                        "EndPoint":       [1.04, 0.14, 0.5]
                                    },
                                    {
                                        "BoundaryType":   "ReflectionConstraint",
                                        "Norm":           [0, -1., 0],
                                        "StartPoint":     [0., 0., 0.],
                                        "EndPoint":       [1.04, 0.02, 0.5]
                                    },
                                    {
                                        "BoundaryType":   "ReflectionConstraint",
                                        "Norm":           [0, 1., 0],
                                        "StartPoint":     [0, 0.12, 0],
                                        "EndPoint":       [1.04, 0.14, 0.5]
                                    }])

# 11. 저장할 데이터 선택 및 시뮬레이션 실행
mpm.select_save_data()
mpm.run()
mpm.postprocessing()