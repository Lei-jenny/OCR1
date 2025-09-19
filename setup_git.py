#!/usr/bin/env python3
"""
Script to help set up Git repository for GitHub upload
"""
import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_git_installed():
    """Check if Git is installed"""
    print("🔍 Checking Git installation...")
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Git is installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ Git not found")
            return False
    except FileNotFoundError:
        print("❌ Git not found in PATH")
        return False

def setup_git_repo():
    """Set up Git repository"""
    print("\n🔧 Setting up Git repository...")
    
    # Check if already a git repo
    if os.path.exists('.git'):
        print("⚠️ Git repository already exists")
        return True
    
    # Initialize git repository
    if run_command('git init', 'Initializing Git repository'):
        print("✅ Git repository initialized")
        return True
    return False

def add_files():
    """Add files to Git"""
    print("\n📁 Adding files to Git...")
    
    # Add all files
    if run_command('git add .', 'Adding files to Git'):
        print("✅ Files added to Git")
        return True
    return False

def create_initial_commit():
    """Create initial commit"""
    print("\n💾 Creating initial commit...")
    
    if run_command('git commit -m "Initial commit: OCR Menu Detector"', 'Creating initial commit'):
        print("✅ Initial commit created")
        return True
    return False

def show_next_steps():
    """Show next steps for GitHub upload"""
    print("\n" + "="*60)
    print("🎉 Git repository setup complete!")
    print("="*60)
    print("\n📋 Next steps:")
    print("1. Go to GitHub.com and create a new repository")
    print("2. Name it: 'ocr-menu-detector'")
    print("3. Make it public (for free Vercel deployment)")
    print("4. Don't initialize with README (you already have one)")
    print("5. Copy the repository URL")
    print("\n🔗 Then run these commands:")
    print("git remote add origin https://github.com/YOUR_USERNAME/ocr-menu-detector.git")
    print("git branch -M main")
    print("git push -u origin main")
    print("\n☁️ After GitHub upload:")
    print("1. Go to vercel.com")
    print("2. Import your GitHub repository")
    print("3. Deploy!")
    print("\n📖 See DEPLOYMENT_GUIDE.md for detailed instructions")

def main():
    """Main setup function"""
    print("🍽️ OCR Menu Detector - Git Setup")
    print("="*50)
    
    # Check Git installation
    if not check_git_installed():
        print("\n❌ Git is not installed. Please install Git first:")
        print("Download from: https://git-scm.com/downloads")
        return
    
    # Set up repository
    if not setup_git_repo():
        print("❌ Failed to set up Git repository")
        return
    
    # Add files
    if not add_files():
        print("❌ Failed to add files to Git")
        return
    
    # Create commit
    if not create_initial_commit():
        print("❌ Failed to create initial commit")
        return
    
    # Show next steps
    show_next_steps()

if __name__ == '__main__':
    main()
