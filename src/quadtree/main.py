import numpy as np
import time
from quadtree import Quadtree, Point2d
from view import Visualizer
from controller import Controller
import time

import threading
def thread0(controller):
    while 1:
        raw_data = np.random.rand(10, 2) * 400 - 200

        for x, y in raw_data:
            ret = controller.insert_data(x, y)

        x, y = np.random.rand(2,) * 400 - 200
        radius = np.random.randint(20, 50, (1,))
        # radius = 400
        # print(radius)
        controller.query_circle(x, y, radius)
        controller.delete_data()

        x, y = np.random.rand(2,) * 400 - 200
        w, h = np.random.randint(20, 200, (2,))
        controller.query_rect(x, y, w, h)
        controller.delete_data()

        # time.sleep(0.6)

        time.sleep(0.1)


if __name__ == "__main__":
    # np.random.seed(123)
    n = 100
    data_lim = (-200, -200, 200, 200)
    query_box_size = (50, 50)
    circle_radius = 20

    model = Quadtree(*data_lim, 0, 1, 6, "Root")
    view = Visualizer(data_lim=data_lim, 
                    rect_size=query_box_size,
                    circle_radius=circle_radius)
    controller = Controller(model, view)

    # raw_data = np.random.rand(1000, 2) * 400 - 200
    # for x, y in raw_data:
        # ret = controller.insert_data(x, y)

    # th0 = threading.Thread(target=thread0, args=(controller,))
    # th0.daemon = True
    # th0.start()

    view.run()
    # th0.join()
