import os
import sys
import time

import numpy as np
import pybullet as p
import pybullet_data

if __name__ == "__main__":
    urdf_path = os.path.abspath("urdfs/doggo-arm/urdf/doggo-arm.urdf")

    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)
    dt = 1./240.

    plane = p.loadURDF("plane.urdf", [0,0,-0.001])
    robot = p.loadURDF(urdf_path, [0,0,0.001], useFixedBase=True)

    dof = p.getNumJoints(robot)

    joint_positions = [0, 0, 0]*dof
    sliders = []
    
    for j in range(dof):
        joint_info = p.getJointInfo(robot, j)
        print(joint_info)
        sliders.append(p.addUserDebugParameter(f"Joint {j}", -np.pi/2, np.pi/2, 0))
        p.setJointMotorControl2(robot, j, p.VELOCITY_CONTROL, force=0)
        p.changeDynamics(robot, j, jointLowerLimit=-np.pi/2, jointUpperLimit=np.pi/2)


    while True:
        for j in range(dof):
            joint_positions[j] = p.readUserDebugParameter(sliders[j])
            p.setJointMotorControl(robot, j, p.POSITION_CONTROL, joint_positions[j])

        p.stepSimulation()
        time.sleep(dt)

    p.disconnect()
    sys.exit(0)