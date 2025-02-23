import subprocess

# Start app-server.py
app_server = subprocess.Popen(['python', 'app-server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Start corpus-server.py
corpus_server = subprocess.Popen(['python', 'corpus-server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Start dictionary-server.py
dictionary_server = subprocess.Popen(['python', 'dictionary-server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Function to print stdout and stderr
def print_output(process, name):
    for line in process.stdout:
        print(f'[{name} stdout] {line.decode().strip()}')
    for line in process.stderr:
        print(f'[{name} stderr] {line.decode().strip()}')

# Print output for each server
print_output(app_server, 'app-server')
print_output(corpus_server, 'corpus-server')
print_output(dictionary_server, 'dictionary-server')