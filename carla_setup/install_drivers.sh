echo "Updating system..."
sudo apt update && sudo apt upgrade -y

echo "Installing NVIDIA drivers..."
sudo apt install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall

echo "Installing Python dependencies..."
pip3 install -r ../requirements.txt

echo "Done! Reboot the VM now with: sudo reboot"