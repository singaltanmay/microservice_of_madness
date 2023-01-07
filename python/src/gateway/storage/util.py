import pika, json

def upload(f, fs, channel, access):
    try:
        fid = fs.put(f)
    except Exception as err:
        return "Internal Server Error", 500

    message = {
        "video_fid": str(fid),
        "mp3_field": None,
        "username": access["username"]
    }

    try:
        channel.basic_public(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTANT_DELIVERY_MODE
            ),
        )
    except:
        fs.delete(fid)
        return "Internal Server Error", 500