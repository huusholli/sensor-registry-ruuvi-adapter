# RUUVI-ADAPTER

Adapter between RuuviTags and [Sensor Registry](https://github.com/huusholli/sensor-registry)

## Installation

Better to follow instructions described here:

https://github.com/ttu/ruuvitag-sensor/blob/master/install_guide_pi.md

## Run as systemd service

Example configuration is as follows

```
# /etc/systemd/system/ruuvi-adapter.service
# start on boot: sudo systemctl enable ruuvi-adapter

[Unit]
Description=RuuviTag Adapter for Sensor Registry
After=network.target

[Service]
ExecStart=/usr/bin/python app.py
WorkingDirectory=/home/pi/ruuvi-adapter
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi
Environment="SENSOR_REGISTRY_HOST=http://path-to-sensor-registry"

[Install]
WantedBy=multi-user.target
```

## License

MIT
