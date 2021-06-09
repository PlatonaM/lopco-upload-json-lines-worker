## lopco-upload-json-lines-worker

Upload data stored as a JSON object per line via the PlatonM MQTT connector.

### Configuration

`mqtt_server`: Address of the MQTT server (IP or domain).

`mqtt_port`: Open port of MQTT server.

`mqtt_keepalive`: Delay in seconds between keep alive pings.

`mqtt_qos`: MQTT quality of service level (recommended: `2`).

`mqtt_connect_retry`: Number of connection attempts before aborting.

`mqtt_connect_retry_delay`: Delay in seconds between connection attempts.

`mqtt_tls`: Control if the MQTT connection is TLS encrypted (recommended: `1`).

`proxy_type`: Set the type of proxy to `HTTP`, `SOCKS4` or `SOCKS5`.

`proxy_address`: Address of the proxy server.

`proxy_usr`: Username if proxy server requires credentials.

`proxy_pw`: Password if proxy server requires credentials.

`service_id`: ID of the data service as defined in the device type to which the device belongs.

`batch_pos_field`: Field containing positional information.

`batch_pos_start`: Positional identifier for first message of batch.

`batch_pos_intermediate`: Positional identifier for messages between start and end of batch.

`batch_pos_end`: Positional identifier for last message of batch.

`usr`:  Username.

`pw`: Password.

### Inputs

Type: single

`source_file`: File with a JSON object per line.

### Outputs

None

### Description

    {
        "name": "Upload JSON Lines",
        "image": "platonam/lopco-upload-json-lines-worker:dev",
        "data_cache_path": "/data_cache",
        "description": "Upload JSON objects stored per line from file.",
        "configs": {
            "mqtt_server": null,
            "mqtt_port": null,
            "mqtt_keepalive": "5",
            "mqtt_qos": "2",
            "mqtt_connect_retry": "10",
            "mqtt_connect_retry_delay": "30",
            "mqtt_tls": "1",
            "proxy_type": null,
            "proxy_address": null,
            "proxy_usr": null,
            "proxy_pw": null,
            "service_id": null,
            "batch_pos_field": null,
            "batch_pos_start": null,
            "batch_pos_intermediate": null,
            "batch_pos_end": null,
            "usr": null,
            "pw": null
        },
        "input": {
            "type": "single",
            "fields": [
                {
                    "name": "source_file",
                    "media_type": "text/plain",
                    "is_file": true
                }
            ]
        },
        "output": null
    }
