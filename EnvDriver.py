import threading
import subprocess
import redis
redis_client = redis.Redis(
    host='redis-19800.crce179.ap-south-1-1.ec2.redns.redis-cloud.com',
    port=19800,
    decode_responses=True,
    username="default",
    password="JMPog04EGI2MVcbO3HDPC9clDNyztfBX",
)

# Initialize Redis client
# Dictionary to keep track of running processes
processes = {}

def run_scrapper(scrapper_name):
    if scrapper_name == 'amazon':
        print("Running Amazon scrapper")
        process = subprocess.Popen(['python', 'AmazonScrapper.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    elif scrapper_name == 'flipkart':
        print("Running Flipkart scrapper")
        process = subprocess.Popen(['python', 'FlipkartScrapper.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    elif scrapper_name == 'quora':
        print("Running Quora scrapper")
        process = subprocess.Popen(['python', 'QuoraScrapper.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    elif scrapper_name == 'combined':
        print("Running Combined scrapper")
        process = subprocess.Popen(['python', 'CombinedScrapper.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    else:
        print('Invalid scrapper name')
        return None

    # Print the output of the subprocess in real-time
    def print_output(process):
        for line in process.stdout:
            print(line.strip())
        for line in process.stderr:
            print(line.strip())

    threading.Thread(target=print_output, args=(process,), daemon=True).start()
    return process

def stop_scrapper(scrapper_name):
    if scrapper_name in processes:
        processes[scrapper_name].terminate()
        del processes[scrapper_name]
        print(f"Stopped {scrapper_name} scrapper")
    else:
        print(f"No running scrapper found with name {scrapper_name}")

def handle_redis_message(message):
    command, scrapper_name = message.split()
    if command == 'start':
        if scrapper_name in processes:
            print(f"{scrapper_name} scrapper is already running")
        else:
            process = run_scrapper(scrapper_name)
            if process:
                processes[scrapper_name] = process
    elif command == 'stop':
        stop_scrapper(scrapper_name)
    else:
        print(f"Unknown command: {command}")

def listen_to_redis():
    pubsub = redis_client.pubsub()
    pubsub.subscribe('scrapper_commands')
    for message in pubsub.listen():
        if message['type'] == 'message':
            handle_redis_message(message['data'])

if __name__ == '__main__':
    redis_thread = threading.Thread(target=listen_to_redis, daemon=True)
    redis_thread.start()

    # Keep the main thread alive
    while True:
        pass