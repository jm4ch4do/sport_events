from api import app

# for deploy using gunicorn in render.com
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
