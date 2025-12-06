import subprocess
import sys

def install_package(package_name):
    
    print(f"Installing package: {package_name}")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"Successfully installed {package_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}. Error: {e}")
        sys.exit(1)

REQUIRED_PACKAGES = ["flask-login", "flask", "requests", "flask-bcrypt", "flask-wtf", "flask-mail", "pymongo", "dotenv", "email_validator", "flask_cors", "flask_jwt_extended"]

def main():
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package.replace("-", "_"))
            print(f"Package {package} is already installed.")
        except ImportError:
            install_package(package)
    print("All required packages are installed.")

if __name__ == "__main__":
    main()