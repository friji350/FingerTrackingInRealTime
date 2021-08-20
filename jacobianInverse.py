import numpy as np
import math
import matplotlib.pyplot as plt
from RobotArm import *
import serial
import time
import telnetlib
Arm = RobotArm2D()
telnet = telnetlib.Telnet('192.168.43.54')
Arm.add_revolute_link(length=19.7, thetaInit=math.radians(90))
Arm.add_revolute_link(length=18.5, thetaInit=math.radians(90))
Arm.add_revolute_link(length=9, thetaInit=math.radians(90))

Arm.update_joint_coords()

target = Arm.joints[:,[-1]]

fig, ax = plt.subplots(figsize=(5,5))
fig.subplots_adjust(left=0, bottom=0, right=1, top=1)
targetPt, = ax.plot([], [], marker='o', c='r')
endEff, = ax.plot([], [], marker='o', markerfacecolor='w', c='g', lw=2)
armLine, = ax.plot([], [], marker='o', c='g', lw=2)

reach = sum(Arm.lengths)

ax.set_xlim(Arm.xRoot - 1.2 * reach, Arm.xRoot + 1.2 * reach)
ax.set_ylim(Arm.yRoot - 1.2 * reach, Arm.yRoot + 1.2 * reach)

circle = plt.Circle((Arm.xRoot, Arm.yRoot), reach, ls='dashed', fill=False)
ax.add_artist(circle)

def update_plot():
    armLine.set_data(Arm.joints[0,:-1], Arm.joints[1,:-1])
    endEff.set_data(Arm.joints[0,-2::], Arm.joints[1,-2::])

update_plot()

def move_to_target(angle):
    global Arm, target, reach

    # Set distance to move end effector toward target per algorithm iteration.
    distPerUpdate = 0.02 * reach



    if np.linalg.norm(target - Arm.joints[:,[-1]]) > 0.02 * reach:
        targetVector = (target - Arm.joints[:,[-1]])[:3]
        targetUnitVector = targetVector / np.linalg.norm(targetVector)
        deltaR = distPerUpdate * targetUnitVector
        J = Arm.get_jacobian()
        JInv = np.linalg.pinv(J)
        deltaTheta = JInv.dot(deltaR)
        Arm.update_theta(deltaTheta)
        Arm.update_joint_coords()
        print("try")
        if math.degrees(Arm.thetas[0]) > 65 and math.degrees(Arm.thetas[0]) < 180:
            s = f'A{angle} B{round(math.degrees(Arm.thetas[0]))} C{180 - round(math.degrees(Arm.thetas[1]))} D{round(math.degrees(Arm.thetas[2])) + 30}\n'
            print("send")

            telnet.write(s.encode())
            time.sleep(0.05)

        update_plot()
    else:
        return 1


mode = 1

def on_button_press(event):
    global target, targetPt
    xClick = event.xdata
    yClick = event.ydata

    go_to(xClick, yClick)
fig.canvas.mpl_connect('button_press_event', on_button_press)

def go_to(xClick,yClick,angle):

    global target, targetPt

    a = 0
    exit_ = True

    if  isinstance(xClick, float) and isinstance(yClick, float):
        targetPt.set_data(xClick, yClick)
        target = np.array([[xClick - 3.5, yClick - 11.0, 0, 1]]).T

    while exit_:
        print(xClick)
        if move_to_target(angle) == 1:
            exit_ = False


exitFlag = False

def on_key_press(event):

    global exitFlag, mode
    if event.key == 'enter':
        exitFlag = True
    elif event.key == 'shift':
        mode *= -1
fig.canvas.mpl_connect('key_press_event', on_key_press)

plt.ion()
plt.show()

print('Select plot window and press Shift to toggle mode or press Enter to quit.')

t = 0.
l = 0


#while not exitFlag:
#    if mode == -1:
#        targetX = Arm.xRoot + 1.1 * (math.cos(0.12*t) * reach) * math.cos(t)
#        targetY = Arm.yRoot + 1.1 * (math.cos(0.2*t) * reach) * math.sin(t)
#        targetPt.set_data(targetX, targetY)
#        target = np.array([[targetX, targetY, 0, 1]]).T
#        t += 0.025
    #if l == 0:
    #    go_to(-25.1231321421, 15.1231321421)
    #    move_to_target()
    #    l+=1
    #go_to(-25.03, 15.03)
#    move_to_target()
#    fig.canvas.get_tk_widget().update()
