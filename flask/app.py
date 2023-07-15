import json
import os
import shutil

from flask import Flask, request, render_template

app = Flask(__name__, template_folder='./public', static_folder='./public/static')

config_dir = 'config'
config_file_path = config_dir + '/config.json'
default_config_path = 'default-config.json'


def check_config():
    if not os.path.exists(config_file_path):
        try:
            os.makedirs(config_dir)
        finally:
            shutil.copy(default_config_path, config_file_path)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/preference', methods=['POST'])
def save_preference():
    with open(config_file_path, 'r', encoding='utf8') as config_file:
        config = json.load(config_file)
        config_file.close()

    with open(config_file_path, 'w', encoding='utf8') as config_file:
        for key in request.get_json():
            config[key] = request.get_json()[key]

        json.dump(config, config_file, indent=4, ensure_ascii=False)
        config_file.close()

    return {'success': True}


@app.route('/api/preference', methods=['GET'])
def get_preference():
    with open(config_file_path, 'r', encoding='utf8') as config_file:
        config = json.load(config_file)
        config_file.close()

    config['rpc-listen-port'] = os.environ.get('RPC_PORT')
    config['rpc-host'] = os.environ.get('RPC_HOST')
    config['rpc-secret'] = os.environ.get('RPC_SECRET')
    return config


if __name__ == '__main__':
    check_config()
    app.run(debug=False, host="0.0.0.0")
