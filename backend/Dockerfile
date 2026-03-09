# LICENSE UPL
# Author: Mauro Risonho de Paula Assumpção
# Description: 
FROM rockylinux:9

# Disable fastestmirror and configure networking for robust DNF operations
RUN echo "fastestmirror=False" >> /etc/dnf/dnf.conf && \
    echo "max_parallel_downloads=10" >> /etc/dnf/dnf.conf

# Install Epel, Python 3.9 and required dev tools
RUN dnf install -y epel-release && \
    dnf update -y && \
    dnf install -y python3 python3-pip python3-devel gcc gcc-c++ make sqlite \
    && dnf clean all

WORKDIR /app

# Upgrade pip to avoid issues with modern wheels
RUN pip3 install --upgrade pip

# We copy the requirements file first to cache the layer
COPY backend/requirements.txt .

# Install dependencies preferring binaries to avoid compilation overhead inside Rocky
RUN pip3 install --no-cache-dir --prefer-binary -r requirements.txt

# Create an empty db file to prevent ownership issues if mapped as a volume
RUN mkdir -p /app/data && touch /app/data/telemetry.db && chmod 664 /app/data/telemetry.db

CMD ["python3", "-m", "uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]
