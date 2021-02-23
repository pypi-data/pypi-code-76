from direct.directbase.DirectStart import base
from panda3d.core import*


def main():
    window = WindowProperties()
    window.setTitle("Fly to the universe")
    window.setSize(1200, 900)
    base.win.requestProperties(window)
    base.setBackgroundColor(0/255, 128/255, 255/255)
    schoolKey = loader.loadModel("images_window/school")
    schoolKey.reparentTo(render)
    space = loader.loadModel("images_window/space")
    space.reparentTo(render)
    space.setScale(0.7)
    space.setPos(0, -500, 0)
    base.run()


if __name__ == "__main__":
    main()
