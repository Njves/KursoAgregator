from app import create_app
import client

app = create_app()
if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()
    # client.execute()