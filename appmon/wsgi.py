from app import create_app

if __name__ == '__main__':
    app_mon = create_app(app_name="flask_appmon")
    app_mon.run(port=8080)
