import paramiko
import time

host = "45.134.217.246"
password = "7FggQR5ePIVZ"

print("Connecting to remote server...")
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username="root", password=password)
print("Connected!")

commands = [
    "apt-get update -y",
    "apt-get install -y tinyproxy",
    "sed -i 's/^Allow /#Allow /g' /etc/tinyproxy/tinyproxy.conf",
    "grep -q 'BasicAuth stepansky 7FggQR5ePIVZ' /etc/tinyproxy/tinyproxy.conf || echo 'BasicAuth stepansky 7FggQR5ePIVZ' >> /etc/tinyproxy/tinyproxy.conf",
    "systemctl restart tinyproxy",
    "systemctl status tinyproxy --no-pager"
]

for cmd in commands:
    print(f"Running: {cmd}")
    stdin, stdout, stderr = client.exec_command(cmd)
    
    # Wait for the command to finish
    exit_status = stdout.channel.recv_exit_status()
    
    print("STDOUT:\n" + stdout.read().decode(errors='ignore').strip())
    err = stderr.read().decode(errors='ignore').strip()
    if err:
        print("STDERR:\n" + err)

client.close()
print("Proxy configured successfully!")
