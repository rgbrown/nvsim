from sympy.abc import _clash
from sympy import sympify, Eq
from IPython.display import display
from mako.template import Template



class nvmodel:
    def __init__(self, parameters, algebraic, ode):
        self.parameters = parameters
        self.algebraic = algebraic
        self.ode = ode
        self.idx_algebraic = dict(zip(algebraic.keys(), range(len(algebraic))))
        self.idx_state = dict(zip(ode.keys(), range(len(ode))))

    def display(self):
        print("Parameters:")
        for key in self.parameters:
            display(Eq(sympify(key, _clash), sympify(self.parameters[key], _clash)))

        print("\nAlgebraic equations:")
        for key in self.algebraic:
            display(Eq(sympify(key, _clash), sympify(self.algebraic[key], _clash)))
                
        print ("\nState variables:")
        for key in self.ode:
            display(Eq(sympify("d{:s}/dt".format(key)), sympify(self.ode[key], _clash)))

    def generate_c(self):
        mytemplate = Template(filename='templates/template.c')
        return mytemplate.render(model=self)
    
    def generate_matlab(self):
        mytemplate = Template(filename='templates/template.m')
        return mytemplate.render(model=self)


def load_model(filename):
    """ load model from file. 

    arguments:
    filename: the location of the model text file. The file should be of
    the following format
    # parameters
    a = 3
    b = 2.5

    #algebraic
    f = 3*x + a

    # ode
    dx = 3*f + b*a

    The ode, algebraic, and parameters blocks can be interspersed in any
    order and occur multiple times
    """


    with open(filename) as f:
        lines = f.readlines()
        
    class mode_enum:
        parameters, algebraic, ode = range(3)
        
    parameters = {}
    algebraic = {}
    ode = {}
    for line in lines:
        if line[0] == '#':
            mode_str = line.strip('#').strip().lower()
            if mode_str == "parameters":
                mode = mode_enum.parameters
            elif mode_str == "algebraic":
                mode = mode_enum.algebraic
            elif mode_str == "ode":
                mode = mode_enum.ode
            else:
                raise RuntimeError("unknown mode")
        else:
            if line.strip() == "":
                continue
            
            items = [s.strip() for s in line.split('=')]
            if mode == mode_enum.parameters:
                parameters.update({items[0]: sympify(items[1], _clash)})
            elif mode == mode_enum.algebraic:
                algebraic.update({items[0]: sympify(items[1], _clash)})
            elif mode == mode_enum.ode:
                assert items[0][0].lower() == 'd' 
                ode.update({items[0][1:]: sympify(items[1], _clash)})

    return nvmodel(parameters, algebraic, ode)
        
if __name__ == "__main__":
    model = load_model('models/fitz2.txt')
    model.display()
    print model.generate_c()
    print model.generate_matlab()
