from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run-docker', methods=['POST'])
def run_docker():
    github_url = request.json.get('GITHUB_URL')
    user_id = request.json.get('USER_ID')

    if not github_url or not user_id:
        return jsonify({'error': 'Missing parameters'}), 400

    try:
        command = [
            'sudo','docker', 'run', '--rm',
            '-v', '/var/run/docker.sock:/var/run/docker.sock',
            '-e', f'GITHUB_URL={github_url}',
            '-e', f'USER_ID={user_id}',
            'nixpacks_builder'
        ]
        
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return jsonify({
            'stdout': result.stdout.decode('utf-8'),
            'stderr': result.stderr.decode('utf-8'),
            'returncode': result.returncode
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
