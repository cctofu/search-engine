import subprocess
import json

def search_api(query):
    url = 'http://101.6.161.39:8000/api/search'
    data = json.dumps({'query': query})
    
    result = subprocess.run(
        ['curl', '-X', 'POST', '-d', data, url],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    stdout_output = result.stdout.decode('utf-8')
    stderr_output = result.stderr.decode('utf-8')
    
    print("STDOUT:", stdout_output)
    print("STDERR:", stderr_output)
    
    if result.returncode == 0:
        try:
            return json.loads(stdout_output)
        except json.JSONDecodeError as e:
            print("JSONDecodeError:", e)
            return {'error': 'Invalid JSON response', 'response': stdout_output}
    else:
        return {'error': result.returncode, 'message': stderr_output}

# Example usage
query = "your search query here"
result = search_api(query)
print(result)
