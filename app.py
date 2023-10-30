from mvc import *

# instantiation of the controller object from MVC design pattern
controller = Controller(Model(), View())
print("\nWelcome")
controller.run()
