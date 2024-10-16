import numpy as np
import time
from octree import Octree, Point3d
from view import Visualizer
from controller import Controller
import time

import threading
def thread0(controller):
    while 1:
        # raw_data = np.random.rand(10, 3) * 400 - 200

        # for x, y, z in raw_data:
            # ret = controller.insert_data(x, y, z)

        x, y, z = np.random.rand(3,) * 400 - 200
        radius = np.random.randint(20, 100, (1,))
        controller.query_circle(x, y, z, radius)
        # controller.delete_data()
        time.sleep(0.5)


if __name__ == "__main__":
    # np.random.seed(123)
    n = 100
    data_lim = (-200, -200, -200, 200, 200, 200)
    query_box_size = (0,0,0,350,350,350)
    circle_radius = 20

    model = Octree(*data_lim, 0, 1, 5, "Root")
    view = Visualizer(data_lim=data_lim,
                    query_box_size=None,
                    circle_radius=circle_radius)
    controller = Controller(model, view)

    raw_data = np.random.rand(50, 3) * 400 - 200
    for x, y, z in raw_data:
        ret = controller.insert_data(x, y, z)

    controller.query_rect(*query_box_size)
    # controller.query_circle(0,0,0, 250)
    controller.delete_data()

    # print(model)

    # th0 = threading.Thread(target=thread0, args=(controller,))
    # th0.daemon = True
    # th0.start()

    view.run()
    # th0.join()
