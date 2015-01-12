parameters = {
        'a': 0.7,
        'b': 0.8,
        'tau': 12.5,
        'I': 0.5
        }
algebraic = {
        'f': 'v - v**3/3 -w + I',
        'g': 'v + a - b*w'
        }
state = {
        'v': 'f',
        'w': 'g / tau'
        }
