from calc_model import Model
from calc_controller import Controller
from calc_view import View


if __name__ == '__main__':
    model = Model()
    view = View()
    controller = Controller(model, view)
    view.set_controller(controller)
    controller.run()
