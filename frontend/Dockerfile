# LICENSE UPL
# Author: Mauro Risonho de Paula Assumpção
# Description: 
FROM rockylinux:9

# Disable fastestmirror
RUN echo "fastestmirror=False" >> /etc/dnf/dnf.conf

# Install Node.js 20 from NodeSource since Rocky 9 default is older
RUN curl -fsSL https://rpm.nodesource.com/setup_20.x | bash - && \
    dnf install -y nodejs && \
    dnf clean all

WORKDIR /app

# Copy package info and install
COPY package.json package-lock.json* ./
RUN npm install

# Copy application source
COPY . .

# Expose Vite dev port
EXPOSE 3000

# Run Vite dev server bound to all interfaces
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
