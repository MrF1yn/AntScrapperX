import os
import subprocess


def run_scrapper():
    scrapper_name = os.getenv('SCRAPPER_NAME')
    if scrapper_name == 'amazon':
        print("Running Amazon scrapper")
        process = subprocess.Popen(['python', 'AmazonScrapper.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True)
    elif scrapper_name == 'flipkart':
        print("Running Flipkart scrapper")
        process = subprocess.Popen(['python', 'FlipkartScrapper.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True)
    elif scrapper_name == 'quora':
        print("Running Quora scrapper")
        process = subprocess.Popen(['python', 'QuoraScrapper.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True)
    else:
        print('Invalid scrapper name')
        return

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    # print('Output:', result.stdout)
    print('Error:', process.stderr)


if __name__ == '__main__':
    run_scrapper()
