<%!
import sympy
from sympy.printing import octave_code
%>

function params = parse_inputs(varargin)
p = inputParser()
% for key in model.parameters:
p.addParameter('${key}', ${octave_code(model.parameters[key])});
% endfor
p.parse(varargin{:})
params = p.Results;
end


% for key in model.parameters:
${key + ' = ' + octave_code(model.parameters[key]) + ';'}
% endfor

function alg = algebraic(u, t)
% for key in model.ode:
    ${key + ' = ' + 'u(' + (model.idx_state[key] + 1).__str__() + ', :);'}
% endfor

% for key in model.algebraic:
    ${key + ' = ' + octave_code(model.algebraic[key]) + ';'}
% endfor 

% for key in model.algebraic:
    alg = zeros(${}, size(u, 2));
    ${'alg(' + (model.idx_algebraic[key] + 1).__str__() + ', :) = ' + key + ';' }
% endfor
end

function du = ode(u, t, alg)
%% Extract algebraic and state variables
% for key in model.algebraic:
    ${key + ' = ' + 'alg(' + (model.idx_algebraic[key] + 1).__str__() + ', :);'}
% endfor
% for key in model.ode:
    ${key + ' = ' + 'u(' + (model.idx_state[key] + 1).__str__() + ', :);'}
% endfor
    
%% ODE Right hand sides 
    du = zeros(size(u));
% for key in model.ode:
    ${'du(' + (model.idx_state[key] + 1).__str__() + ', :) = ' + octave_code(
            model.ode[key]) + ';'}
% endfor
end
