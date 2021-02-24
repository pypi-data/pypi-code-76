from direct.directbase.DirectStart import base
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import *
from direct.actor.Actor import Actor


# 自定义加载模型函数
def load_model(path, pos, hpr):
    model = loader.loadModel(path)
    model.reparentTo(render)
    model.setPos(pos[0], pos[1], pos[2])
    model.setHpr(hpr[0], hpr[1], hpr[2])
    return model


def main():
    # 设置窗体属性
    window = WindowProperties()
    window.setTitle("bridge")
    window.setSize(1200, 800)
    base.win.requestProperties(window)
    base.setBackgroundColor(100/255, 150/255, 180/255)
    # 设置镜头参数
    base.cam.setPos(-5800, -3750, 3300)
    base.cam.setHpr(0, -46, 0)
    # 禁用鼠标控制
    base.disableMouse()

    # 加载场景模型
    scene = load_model("images_house/scene", (0, 0, 0), (0, 0, 0))
    house = load_model("images_house/house", (-650, 1500, 0), (45, 0, 0))
    lamp = load_model("images_house/lamp", (-800, 800, 0), (-90, 0, 0))
    # 加载太阳能汽车模型
    car = Actor("images_house/car", {"run": "images_house/car_run"})
    car.reparentTo(render)
    car.setHpr(-90, 0, 0)
    car.setPos(-4150, -450, 0)

    # 太阳能汽车的移动状态
    car_state = {"forward": False, "turn_left": False, "turn_right": False}

    # 定义任务函数
    def move(task):
        moving = False
        if car_state["forward"]:
            car.setY(car, -10)
            moving = True
        if car_state["turn_left"]:
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

    # 定义太阳能汽车控制事件函数
    def change_car_state(direction, temp_state):
        car_state[direction] = temp_state

    # 定义键盘事件
    base.accept("w", change_car_state, ["forward", True])
    base.accept("w-up", change_car_state, ["forward", False])
    base.accept("a", change_car_state, ["turn_left", True])
    base.accept("a-up", change_car_state, ["turn_left", False])
    base.accept("s", change_car_state, ["turn_right", True])
    base.accept("s-up", change_car_state, ["turn_right", False])
    
    # 设置悬崖和桥
    cliff = loader.loadModel("images_house/cliff")
    cliff.reparentTo(render)
    bridge = loader.loadModel("images_house/bridge")
    bridge.reparentTo(render)

    # 创建碰撞体
    capsule_down = CollisionCapsule(-6900, -680, 0, -5100, -680, 0, 20)
    collision_down_node = CollisionNode("bridge")
    collision_down_node.addSolid(capsule_down)
    capsule_down_node = render.attachNewNode(collision_down_node)
    # capsule_down_node.show()

    capsule_up = CollisionCapsule(-6900, -160, 0, -5100, -160, 0, 20)
    collision_up_node = CollisionNode("bridge")
    collision_up_node.addSolid(capsule_up)
    capsule_up_node = render.attachNewNode(collision_up_node)
    # capsule_up_node.show()

    # 配置移动碰撞体
    sphereLeft = CollisionSphere(90, -125, 30, 30)
    sphereLeftNode = CollisionNode("car")
    sphereLeftNode.addSolid(sphereLeft)
    sphereLeftCollision = car.attachNewNode(sphereLeftNode)
    # sphereLeftCollision.show()

    sphereRight = CollisionSphere(-90, -125, 30, 30)
    sphereRightNode = CollisionNode("car")
    sphereRightNode.addSolid(sphereRight)
    sphereRightCollision = car.attachNewNode(sphereRightNode)
    # sphereRightCollision.show()

    # 处理推回机制
    pusher = CollisionHandlerPusher()
    pusher.addCollider(sphereLeftCollision, car)
    base.cTrav = CollisionTraverser()
    base.cTrav.addCollider(sphereLeftCollision, pusher)
    pusher.addCollider(sphereRightCollision, car)
    base.cTrav.addCollider(sphereRightCollision, pusher)
    pusher.setHorizontal(True)

    # 运行主函数
    base.run()


if __name__ == "__main__":
    main()
