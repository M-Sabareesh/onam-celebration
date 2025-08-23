#!/usr/bin/env python3
"""
Quick start script for Onam Django project.
This script automates the initial setup process.
"""

import os
import sys
import subprocess
import secrets
import string


def generate_secret_key():
    """Generate a secure Django secret key."""
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(alphabet) for _ in range(50))


def create_env_file():
    """Create .env file from .env.example with generated secret key."""
    if os.path.exists('.env'):
        print("✅ .env file already exists, skipping...")
        return
    
    if not os.path.exists('.env.example'):
        print("❌ .env.example not found")
        return
    
    with open('.env.example', 'r') as f:
        content = f.read()
    
    # Replace placeholder secret key
    secret_key = generate_secret_key()
    content = content.replace('your-secret-key-here-change-in-production', secret_key)
    
    with open('.env', 'w') as f:
        f.write(content)
    
    print("✅ Created .env file with generated secret key")


def run_command(command, description):
    """Run a shell command with description."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is 3.11+."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print(f"❌ Python 3.11+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor} detected")
    return True


def check_for_externally_managed_env():
    """Check if we're in an externally managed environment and provide solutions."""
    try:
        # Try to detect if we're in an externally managed environment
        result = subprocess.run(['python3', '-m', 'pip', 'install', '--help'], 
                              capture_output=True, text=True)
        return False
    except Exception:
        return True


def ensure_virtual_env_creation():
    """Ensure virtual environment can be created, install python3-venv if needed."""
    try:
        # Try to create venv first
        result = subprocess.run(['python3', '-m', 'venv', '--help'], 
                              capture_output=True, text=True)
        return True
    except Exception:
        print("⚠️ python3-venv not found, attempting to install...")
        commands_to_try = [
            'sudo apt update && sudo apt install -y python3-venv python3-full',
            'sudo apt install -y python3-venv',
            'sudo dnf install -y python3-venv',  # For Fedora/RHEL
            'sudo yum install -y python3-venv',  # For older RHEL
        ]
        
        for cmd in commands_to_try:
            print(f"Trying: {cmd}")
            try:
                subprocess.run(cmd, shell=True, check=True)
                print("✅ Successfully installed python3-venv")
                return True
            except subprocess.CalledProcessError:
                continue
        
        print("❌ Could not install python3-venv. Please install it manually:")
        print("  Ubuntu/Debian: sudo apt install python3-venv python3-full")
        print("  Fedora: sudo dnf install python3-venv")
        print("  RHEL/CentOS: sudo yum install python3-venv")
        return False


def main():
    """Main setup function."""
    print("🌸 Onam Django Project Quick Start 🌸")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check for externally managed environment
    if check_for_externally_managed_env():
        print("⚠️ Detected externally managed Python environment")
        print("This script will create a virtual environment to avoid conflicts")
    
    # Ensure we can create virtual environments
    if not ensure_virtual_env_creation():
        return
    
    # Create virtual environment
    if not os.path.exists('venv'):
        print("📦 Creating virtual environment...")
        # Try different venv creation methods
        venv_commands = [
            'python3 -m venv venv',
            'python -m venv venv',
            '/usr/bin/python3 -m venv venv'
        ]
        
        venv_created = False
        for cmd in venv_commands:
            try:
                subprocess.run(cmd, shell=True, check=True, capture_output=True)
                print("✅ Virtual environment created successfully")
                venv_created = True
                break
            except subprocess.CalledProcessError:
                continue
        
        if not venv_created:
            print("❌ Failed to create virtual environment")
            print("Please try manually:")
            print("  python3 -m venv venv")
            print("  source venv/bin/activate  # or venv\\Scripts\\activate on Windows")
            print("  pip install -r requirements.txt")
            return
    else:
        print("✅ Virtual environment already exists")
    
    # Determine activation command based on OS
    if os.name == 'nt':  # Windows
        activate_cmd = 'venv\\Scripts\\activate'
        pip_cmd = 'venv\\Scripts\\pip'
        python_cmd = 'venv\\Scripts\\python'
    else:  # Unix/Linux/macOS
        activate_cmd = 'source venv/bin/activate'
        pip_cmd = 'venv/bin/pip'
        python_cmd = 'venv/bin/python'
    
    # Upgrade pip
    if not run_command(f'{pip_cmd} install --upgrade pip', 'Upgrading pip'):
        return
    
    # Install requirements
    if not run_command(f'{pip_cmd} install -r requirements.txt', 'Installing Python packages'):
        return
    
    # Create .env file
    create_env_file()
    
    # Create necessary directories
    directories = ['logs', 'media/avatars', 'static/css', 'static/js', 'static/images']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✅ Created necessary directories")
    
    # Run Django commands
    django_commands = [
        (f'{python_cmd} manage.py makemigrations', 'Creating database migrations'),
        (f'{python_cmd} manage.py migrate', 'Running database migrations'),
        (f'{python_cmd} manage.py collectstatic --noinput', 'Collecting static files'),
    ]
    
    for command, description in django_commands:
        if not run_command(command, description):
            print(f"⚠️ Warning: {description} failed, you may need to run this manually")
    
    print("\n🎉 Setup completed successfully! 🎉")
    print("\nNext steps:")
    print(f"1. Activate virtual environment: {activate_cmd}")
    print("2. Update .env file with your SMS provider credentials")
    print(f"3. Create superuser: {python_cmd} manage.py createsuperuser")
    print(f"4. Start development server: {python_cmd} manage.py runserver")
    print("\nAccess your app at: http://localhost:8000/")
    print("Admin panel at: http://localhost:8000/admin/")
    print("\n🌸 Happy Onam! ഓണാശംസകൾ! 🌸")


if __name__ == '__main__':
    main()
