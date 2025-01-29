import subprocess
import sys


def install_dependencies(requirements_file):
    with open(requirements_file, 'r') as file:
        for line in file:
            package = line.strip()
            subprocess.run([sys.executable, '-m', 'pip', 'install', package])


if __name__ == '__main__':
    install_dependencies('requirements.txt')
    # Continue with the rest of your script
