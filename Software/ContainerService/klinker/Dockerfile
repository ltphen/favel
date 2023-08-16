FROM debian:11 AS klinker

# Get required software packages
RUN apt-get update
RUN apt-get install -y build-essential curl python2 python2-dev git

# Get required python2 modules
RUN curl --output get-pip.py https://bootstrap.pypa.io/pip/2.7/get-pip.py
RUN python2 get-pip.py

RUN python2 -m pip install cython==0.29.32
RUN python2 -m pip install numpy==1.16.6
RUN python2 -m pip install scipy==1.2.3
RUN python2 -m pip install pandas==0.24.0
RUN python2 -m pip install sklearn==0.0
RUN python2 -m pip install scikit-learn==0.20.3

# Get knowledgestream
RUN git clone 'https://github.com/saschaTrippel/knowledgestream.git'
WORKDIR /knowledgestream
RUN mkdir output

# Install knowledgestream
RUN python2 setup.py build_ext -if
RUN python2 setup.py install

# Get knowledge graph
RUN curl --output data.tar.gz https://uni-paderborn.sciebo.de/s/E98jf2WqzIW9C1W/download
RUN tar -xf data.tar.gz

# Expose port
EXPOSE 4004/tcp

# Start knowledgestream
CMD kstream -m klinker -p 4004
