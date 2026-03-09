# LICENSE UPL
# Author: Mauro Risonho de Paula Assumpção
# Description: RedTeam AI Evasion Fuzzer Container

FROM rockylinux:9

RUN echo "fastestmirror=False" >> /etc/dnf/dnf.conf && \
    echo "max_parallel_downloads=10" >> /etc/dnf/dnf.conf

RUN dnf install -y epel-release && \
    dnf install -y python3 python3-pip gcc python3-devel sqlite && \
    dnf clean all

WORKDIR /app/redteam

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copia tudo para o container
COPY . .

# Usaremos variaveis de ambiente para mapear o path do isolation forest e do host alvo
CMD ["python3", "adversarial_evasion.py"]
