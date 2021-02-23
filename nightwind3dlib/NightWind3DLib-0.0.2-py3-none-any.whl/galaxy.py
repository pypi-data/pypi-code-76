from direct.directbase.DirectStart import base
from panda3d.core import*


def main():
    window = WindowProperties()
    window.setTitle("New Galaxy")
    window.setSize(1600, 1000)
    base.win.requestProperties(window)
    planets = []
    position = [(0, 0, 0), (600, 0, 0), (-900, 0, 0),
                (1200, 0, 0), (1600, 0, 0), (200, 150, 0)]

    for i in range(1, 7):
        planet = loader.loadModel(f"images_galaxy/planet{i}")
        planet.reparentTo(render)
        planet.setPos(position[i - 1][0], position[i - 1][1], position[i - 1][2])
        planets.append(planet)
        planet.hprInterval(9 - i, (360, 0, 0)).loop()

    for i in range(2, 6):
        virtual = render.attachNewNode(f"planet_{i}")
        planets[i - 1].reparentTo(virtual)
        virtual.hprInterval(9 - i, (360, 0, 0)).loop()

    virtual_6 = planets[3].attachNewNode("planet_6")
    planets[5].reparentTo(virtual_6)
    sky = loader.loadModel("images_galaxy/space_sky")
    sky.reparentTo(render)
    base.run()


if __name__ == "__main__":
    main()
