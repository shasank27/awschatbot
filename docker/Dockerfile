FROM public.ecr.aws/lambda/python:3.13-x86_64

# Install zip and other utilities using dnf
RUN dnf install -y zip

# Create destination directory
RUN mkdir -p /opt/python

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt -t /opt/python

# Package the layer
RUN cd /opt && zip -r9 /layer.zip python
