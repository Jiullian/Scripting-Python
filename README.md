# Python Scripts
Welcome to my Python scripts repository! This space contains a number of Python tutorials designed to explore various aspects of network-related Python programming. Below you'll find information on each of the tutorials included in this repository.

## Run
To use one of these scripts, follow these general steps:

Make sure you have Python installed on your system.
Clone this repository on your computer using the git clone command [Repository URL] or simply download the script by clicking on the "Download" button on GitHub.
Navigate to the directory containing the script you wish to use.
Run the script using the python command [script_name.py].
Example:

bash

Copy code

python script1.py

### [TP Python](https://github.com/Jiullian/Scripting-Python/blob/master/TP_Python.py)
The Python tutorial explores the basic features of the Python language, including file manipulation, operating system detection and the use of the argparse module to process command-line arguments. It retrieves information on the operating system and IP addresses, then writes it to a file.

### [TP Subprocess](https://github.com/Jiullian/Scripting-Python/blob/master/TP_Subprocess.py)
The Subprocess TP uses the subprocess module to execute system commands, retrieving information about the operating system, using ifconfig on Linux and ipconfig on Windows. It also explores file creation and directory management.

### [TP Socket](https://github.com/Jiullian/Scripting-Python/blob/master/TP_Socket.py)
TP Socket explores the creation of sockets in Python to perform port scanning on IP addresses. It uses the socket module to attempt to connect to ports on a given network. It can be useful for port discovery or checking host availability.

### [TP Scapy](https://github.com/Jiullian/Scripting-Python/blob/master/TP_Scapy.py)
TP Scapy uses the scapy module to capture and analyze network traffic. It sniffs packets on a selected network interface, records them in a PCAP file, then analyzes source and destination IP address pairs.

### [TP Threading](https://github.com/Jiullian/Scripting-Python/blob/master/TP_Threading.py)
TP Threading uses Python threads to process captured packets more efficiently. It divides the list of packets into two parts, processes them in parallel with two separate threads, then merges the results.

### [TP Multiprocessing](https://github.com/Jiullian/Scripting-Python/blob/master/TP_Multiprocessing.py)
TP Multiprocessing is similar to TP Threading, but instead of using threads, it uses separate processes to process packets in parallel. This can be useful for taking full advantage of multicore processors.

### [TP Joblib](https://github.com/Jiullian/Scripting-Python/blob/master/TP_Joblib.py)
The Joblib TP is similar to the Threading and Multiprocessing TPs, but uses the joblib library to perform parallel processing. joblib offers simple parallelism features to speed up data processing.

