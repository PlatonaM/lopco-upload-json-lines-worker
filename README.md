#### Description

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

Possible values for `proxy_type` config option: `HTTP`, `SOCKS4` and `SOCKS5`