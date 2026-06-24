CARLA_PATH=~/carla  # change this to your CARLA install path

echo "Starting CARLA server in headless mode..."
cd $CARLA_PATH
./CarlaUE4.sh -RenderOffScreen -carla-server -benchmark -fps=20 &

echo "CARLA started. Waiting 15 seconds for server to initialize..."
sleep 15
echo "Ready. You can now run main.py"