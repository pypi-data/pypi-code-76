from direct.directbase.DirectStart import base
from panda3d.core import*
from direct.actor.Actor import Actor


# 设置聚光灯
def spotlight(color, size, pos, hpr):
    spotlight = Spotlight("light")
    spotlight.setColor(color)
    lens = PerspectiveLens()
    lens.setFov(size)
    spotlight.setLens(lens)
    SpotLight = render.attachNewNode(spotlight)
    render.setLight(SpotLight)
    SpotLight.setPos(pos[0], pos[1], pos[2])
    SpotLight.setHpr(hpr[0], hpr[1], hpr[2])
    return SpotLight


def main():
    window = WindowProperties()
    window.setTitle("Celebration")
    window.setSize(1200, 800)
    base.win.requestProperties(window)

    # 加载舞台
    stage = loader.loadModel("images_stage/stage")
    stage.reparentTo(render)

    # 设置镜头角度
    base.cam.setPos(0, -2000, 600)
    base.cam.setHpr(0, -12, 0)

    # 设置聚光灯
    spotlight1 = spotlight((50 / 255, 200 / 255, 180 / 255, 1), 20,
                           (400, -420, 400), (10, -30, 0))

    spotlight2 = spotlight((255 / 255, 50 / 255, 190 / 255, 1), 20,
                           (200, -420, 400), (10, -30, 0))

    spotlight3 = spotlight((160 / 255, 190 / 255, 130 / 255, 1), 20,
                           (-200, -420, 400), (-10, -30, 0))

    spotlight4 = spotlight((160 / 255, 190 / 255, 190 / 255, 1), 20,
                           (-400, -420, 400), (-10, -30, 0))

    spotlight1.hprInterval(1.3, (30, -10, 0)).loop()
    spotlight2.hprInterval(1.2, (-30, -20, 0)).loop()
    spotlight3.hprInterval(1.5, (40, -40, 0)).loop()
    spotlight4.hprInterval(1.1, (-40, -20, 0)).loop()

    # 添加环境光源
    light = AmbientLight("lightNode")
    light.setColor((0.3, 0.3, 0.3, 1))
    ambient_light = render.attachNewNode(light)
    render.setLight(ambient_light)

    # 加载动画
    codemao = Actor("images_stage/codemao", {"dance1": "images_stage/codemao_dance1",
                                             "dance2": "images_stage/codemao_dance2"})
    codemao.reparentTo(render)
    codemao.setPos(0, 0, 100)
    codemao.loop("dance2")

    # 播放动画
    line = NodePath("codemao_line")
    for i in range(-300, 310, 200):
        line_node = line.attachNewNode("codemao")
        codemao.instanceTo(line_node)
        line_node.setPos(i, 150, 0)

    line.reparentTo(render)

    # 运行程序
    base.run()


if __name__ == "__main__":
    main()
