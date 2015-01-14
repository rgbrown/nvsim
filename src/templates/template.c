<%!
import sympy
from sympy.printing import ccode

%>

/* Parameters */
% for key in model.parameters:
static const double ${key + ' = ' + ccode(model.parameters[key]) + ';'}
% endfor

/* Algebraic equations */
void algebraic(double *alg, double *u, double t)
{
% for key in model.ode:
    ${key + ' = ' + 'u[' + model.idx_state[key].__str__() + '];'}
% endfor

% for key in model.algebraic:
    ${key + ' = ' + ccode(model.algebraic[key]) + ';'}
% endfor 

% for key in model.algebraic:
    ${'alg[' + model.idx_algebraic[key].__str__() + '] = ' + key + ';' }
% endfor
}

/* State Variable ODEs */
void state(double *du, double *u, double t, double *alg)
{
    /* Extract algebraic and state variables */
% for key in model.algebraic:
    ${key + ' = ' + 'alg[' + model.idx_algebraic[key].__str__() + '];'}
% endfor
% for key in model.ode:
    ${key + ' = ' + 'u[' + model.idx_state[key].__str__() + '];'}
% endfor
    
    /* ODE Right hand sides */
% for key in model.ode:
    ${'du[' + model.idx_state[key].__str__() + '] = ' + ccode(
            model.ode[key]) + ';'}
% endfor
}
