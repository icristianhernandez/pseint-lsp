sudo apt update
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-setuptools \
    python3-wheel \
    git \
    build-essential \
    curl \
    wget \
    make \
    gcc \
    g++ \
    libc6-dev \
    libffi-dev \
    libssl-dev

cd /app
python3 -m venv .venv --without-pip
source .venv/bin/activate

# Install pip manually using get-pip.py
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
rm get-pip.py

cd /app
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install Pyright globally via npm
sudo npm install -g pyright

chmod +x run_server.sh
chmod +x tests/run_all_tests.py

# Set up pre-commit hooks (optional)
if command -v pre-commit &> /dev/null; then
    pre-commit install
    echo "Pre-commit hooks installed"
fi