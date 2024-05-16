# Networking 

The example is intended as an example for utilizing [pyShark](https://pypi.org/project/pyshark/) in order to get network
insight.

**Requirements**
```requirements.txt
# users should install either WireShark or tshark package
#tshark>=0.0
pyshark>=0.0
nfstream>=0.0
```

**Process**:
1. Store content in a [pcap file](https://www.reviversoft.com/file-extensions/pcap#:~:text=what%20is%20a.pcap%20file%3F%20The.pcap%20file%20extension%20is,analyzing%20the%20network%20characteristics%20of%20a%20certain%20data.)
2. Convert _pcap_ to _CSV_
3. Concert _CSV_ to _JSON_

### Other Sites
* [Intro to pyShark](https://thepacketgeek.com/pyshark/intro-to-pyshark/)
* [Github](https://github.com/KimiNewt/pyshark)
* [Another Example](https://github.com/Ganeshbg/pyshark)

## Network Types

* **NetFlow** is a network protocol developed by Cisco that provides information about network traffic flows. It collects 
information about source and destination IP addresses, port numbers, protocols, and other network traffic details. 
NetFlow can be used to analyze network traffic patterns, identify potential network security threats, and troubleshoot 
network performance issues.
```shell
sudo tcpdump -i eth0 udp port 2055 -w netflow.pcap
```

* **sFlow** is a similar technology to NetFlow, but it is an open standard developed by InMon Corporation. It works by 
sampling packets from the network at the switch or router and sending them to a central collector for analysis. sFlow 
can provide detailed information about network traffic flows, including application and protocol-specific details. 
```shell
sudo tcpdump -i eth0 udp port 6343 -w sflow.pcap
```

* **Gemini** Network is a network monitoring and analysis platform developed by NetScout Systems. It combines the 
functionality of both NetFlow and sFlow, as well as other network monitoring tools, to provide comprehensive visibility 
into network traffic flows. Gemini Network can be used to monitor and troubleshoot network performance issues, identify 
security threats, and optimize network capacity.
```shell
sudo tcpdump -i eth0 udp port 1212 -w gemini-net.pcap
```

## Sample Code
* Options 
```shell
python3.9 $HOME/Sample-Data-Generator/sample_pyshark.py --help
<< COMMENT
:positional arguments:
    interface      Interface to get data from
:optional arguments:
    -h, --help                              show this help message and exit
    --timeout           TIMEOUT             Wait time
    --packet-count      PACKET_COUNT        Amount of packets to add to the packet list (0 will go forever)
    --file-path         FILE_PATH           PCAP file to initially store data in
    --net-flow          [NET_FLOW]          Get NetFlow data
    --sflow             [SFLOW]             Get sFlow data
    --gemini-net        [GEMINI_NET]        Get Gemini-Net data
    --generic-filter    [GENERIC_FILTER]    manually declare a capturing filter
    --only-summary      [ONLY_SUMMARY]      display packet summaries instead of the entire packet contents.
    --view-interfaces   [VIEW_INTERFACES]   get list of possible interfaces
<<

```

* view list of possible interfaces 
```shell
sudo python3.9 $HOME/Sample-Data-Generator/sample_pyshark.py wifidump --view-interfaces
```

* View Summary of data  
```shell
sudo python3.9 $HOME/Sample-Data-Generator/sample_pyshark.py wifidump --timeout 30 --packet-count 10 --only-summary 
<< COMMENT
{
  "id": "0",
  "expiration_id": "0",
  "src_ip": "192.168.86.23",
  "src_mac": "f0:18:98:13:19:67",
  "src_oui": "f0:18:98",
  "src_port": "49789",
  "dst_ip": "52.22.178.50",
  "dst_mac": "08:b4:b1:04:eb:34",
  "dst_oui": "08:b4:b1",
  "dst_port": "443",
  "protocol": "6",
  "ip_version": "4",
  "vlan_id": "0",
  "tunnel_id": "0",
  "bidirectional_first_seen_ms": "1678410448312",
  "bidirectional_last_seen_ms": "1678410448403",
  "bidirectional_duration_ms": "91",
  "bidirectional_packets": "5",
  "bidirectional_bytes": "898",
  "src2dst_first_seen_ms": "1678410448312",
  "src2dst_last_seen_ms": "1678410448403",
  "src2dst_duration_ms": "91",
  "src2dst_packets": "3",
  "src2dst_bytes": "399",
  "dst2src_first_seen_ms": "1678410448402",
  "dst2src_last_seen_ms": "1678410448403",
  "dst2src_duration_ms": "1",
  "dst2src_packets": "2",
  "dst2src_bytes": "499",
  "application_name": "TLS",
  "application_category_name": "Web",
  "application_is_guessed": "0",
  "application_confidence": "6",
  "requested_server_name": "",
  "client_fingerprint": "",
  "server_fingerprint": "",
  "user_agent": "",
  "content_type": ""
}
<<
```

## Testing Tools
The code has not been tested with filtering options. Some potential data generators 
* [Net Flow](https://www.paessler.com/tools/netflowgenerator)
* [sFlow](https://sflow.net/) 
