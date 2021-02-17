#### Description

    {
        "name": "Upload JSON Lines",
        "image": "platonam/lopco-upload-json-lines-worker:dev",
        "data_cache_path": "/data_cache",
        "description": "Upload JSON objects stored per line from file.",
        "configs": {
            "mqtt_server": null,
            "mqtt_port": null,
            "mqtt_keepalive": "10",
            "usr": null,
            "pw": null,
            "service_id": null
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
