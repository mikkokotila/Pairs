# Installing Pairs

This guide will walk you through the process of installing Pairs on your system. Pairs is a Python-based application that can be installed on various operating systems.

## System Requirements

Before installing Pairs, ensure that your system meets the following requirements:

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+ recommended)
- **Python**: Version 3.8 or higher
- **Disk Space**: At least 500 MB of free disk space
- **Memory**: Minimum 4 GB RAM (8 GB or more recommended)
- **Internet Connection**: Required for AI-assisted features and external integrations

## Installation Methods

There are two primary methods to install Pairs:

1. **Clone from GitHub** (recommended for developers or advanced users)
2. **Download and install** (recommended for most users)

### Method 1: Clone from GitHub

If you're comfortable with Git and want to stay up-to-date with the latest changes, you can clone the repository directly from GitHub.

1. Open a terminal or command prompt
2. Navigate to the directory where you want to install Pairs
3. Clone the repository:

```bash
git clone https://github.com/mikkokotila/Pairs.git
```

4. Navigate to the Pairs directory:

```bash
cd Pairs
```

5. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Method 2: Download and Install

For most users, downloading and installing Pairs is the simplest approach.

1. Visit the [Pairs GitHub repository](https://github.com/mikkokotila/Pairs)
2. Click on the "Code" button and select "Download ZIP"
3. Extract the ZIP file to your desired location
4. Open a terminal or command prompt
5. Navigate to the extracted Pairs directory
6. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Verifying the Installation

To verify that Pairs has been installed correctly:

1. Open a terminal or command prompt
2. Navigate to the Pairs directory
3. Run the application:

```bash
python app/app-server.py
```

4. Open a web browser and navigate to `http://localhost:5000`
5. You should see the Pairs interface

If the application starts successfully and you can access the interface, the installation is complete.

## Troubleshooting

If you encounter issues during installation, try the following:

- Ensure that Python 3.8 or higher is installed and in your PATH
- Check that all dependencies were installed correctly
- Verify that you have sufficient permissions to install packages
- If you're behind a firewall or proxy, configure pip to use the appropriate settings

For more detailed troubleshooting, see the [Common Issues](../troubleshooting/common-issues.md) page.

## Next Steps

Now that you have installed Pairs, you can proceed to:

- [First-Time Setup](first-time-setup.md) - Configure your initial settings
- [Interface Overview](interface-overview.md) - Familiarize yourself with the Pairs interface 