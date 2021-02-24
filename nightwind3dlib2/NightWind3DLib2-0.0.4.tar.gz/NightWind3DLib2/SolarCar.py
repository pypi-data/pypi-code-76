from direct.directbase.DirectStart import base
from direct.task.TaskManagerGlobal import taskMgr
from direct.actor.Actor import Actor
from panda3d.core import *


def load_model(path, pos, hpr):
    model = loader.loadModel(path)
    model.reparentTo(render)
    model.setPos(pos[0], pos[1], pos[2])
    model.setHpr(hpr[0], hpr[1], hpr[2])
    return model


def main():
    # 窗体创建及显示设置
    window = WindowProperties()
    window.setTitle("Solar Car")
    window.setSize(1200, 800)
    base.win.requestProperties(window)
    base.setBackgroundColor(100 / 255, 150 / 255, 180 / 255)
    # 设置相机位置及角度
    base.cam.setPos(450, -6800, 2500)
    base.cam.setHpr(0, -16, 0)
    # 禁用鼠标
    # base.disableMouse()
    # 场景环境及房子
    scene = load_model("images_house/scene", (0, 0, 0), (0, 0, 0))
    house = load_model('images_house/house', (-650, 1500, 0), (45, 0, 0))
    # 太阳
    sun = load_model("images_house/sun", (2500, 1000, 1500), (0, 0, 0))
    sun.setColor((255 / 255, 255 / 255, 100 / 255, 1))
    sun.setScale(100)

    # 照明灯
    lamp = load_model("images_house/lamp", (-800, 800, 0), (-90, 0, 0))

    # 加载架子及太阳能电池板
    shelf = load_model("images_house/shelf", (-1800, -900, 0), (90, 0, 0))
    solar_panel = load_model("images_house/solar_panel", (-1800, -900, 120), (90, 60, 0))
    # 加载太阳能汽车
    car = Actor("images_house/car", {'run': 'images_house/car_run'})
    car.reparentTo(render)
    car.setPos(340, -2300, 0)
    car.setHpr(90, 0, 0)

    def move(task):
        moving = False
        if car_state['forward']:
            car.setY(car, -5)
            moving = True
        if car_state['turn_left']:
            car.setH(car, 2)
            moving = True
        if car_state["turn_right"]:
            car.setH(car, -2)
            moving = True

        if moving:
            control = car.getAnimControl("run")
            if not control.isPlaying():
                car.loop("run")
        else:
            car.stop()
        return task.cont

    taskMgr.add(move)
    # 太阳能汽车的移动状态
    car_state = {"forward": False, "turn_left": False, "turn_right": False}

    def change_car_state(direction, temp_state):
        car_state[direction] = temp_state

    base.accept('w', change_car_state, ['forward', True])
    base.accept('w-up', change_car_state, ['forward', False])
    base.accept('a', change_car_state, ['turn_left', True])
    base.accept('a-up', change_car_state, ['turn_left', False])
    base.accept('s', change_car_state, ['turn_right', True])
    base.accept('s-up', change_car_state, ['turn_right', False])
    base.run()


if __name__ == "__main__":
    main()
