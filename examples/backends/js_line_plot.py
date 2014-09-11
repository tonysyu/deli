import numpy as np

from deli.app.js.main import create_plot, show


x = np.linspace(0, 10)
data = np.transpose([x, np.sin(x)]).tolist()

create_plot(data)
show()
