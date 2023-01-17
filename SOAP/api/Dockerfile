FROM python

RUN wget https://github.com/YanisHessini/pysimplesoap/archive/refs/heads/master.zip

RUN unzip master.zip

RUN cd pysimplesoap-master && python setup.py install

# RUN pip install --no-dependencies git+https://github.com/mikelo/pysimplesoap.git@master
RUN pip install requests
