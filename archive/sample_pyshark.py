import argparse
import csv
import json
import os
import pyshark
from nfstream import NFStreamer

FILE_PATH = os.path.expanduser(os.path.expandvars('$HOME/Sample-Data-Generator/data.pcap'))


def __get_interfaces()->list:
    """
    Get a list of supported interfaces
    """
    cap = pyshark.LiveCapture()
    return cap.interfaces


def __create_file(file_path:str=FILE_PATH)->(pyshark.capture.file_capture.FileCapture, str):
    """"
    1. Create file path to store content in (if DNE)
    2. open FileCapture
    :args:
        file_path:str - file to store content in
    :params:
        full_path:str - expand file path
        cap:pyshark.capture.file_capture.FileCapture - declaration for File Capture
    :return:
        cap, full_path (None if fails to create)
    """
    full_path = os.path.expanduser(os.path.expandvars(FILE_PATH))
    if not os.path.isfile(full_path):
        try:
            open(full_path, 'w').close()
        except Exception as error:
            full_path = None
            print(f"Failed to create file {file_path} (Error: {error})")
    if full_path is not None:
        try:
            cap = pyshark.FileCapture(input_file=full_path, keep_packets=True)
        except Exception as error:
            print(f"Failed to create FileCapture")
    return cap, full_path


def __close_file(cap:pyshark.capture.file_capture.FileCapture, file_path:str=FILE_PATH)->bool:
    """
    Close FileCapture
    :args:
        file_path:str - file path
        cap:pyshark.capture.file_capture.FileCapture - declaration for File Capture
    :params:
        status:bool
    :return:
        status
    """
    status = False
    try:
        cap.close()
    except Exception as error:
        status = False
        print(f"Failed to close file {file_path} (Error: {error})")
    return status


def __print_packets(capture:pyshark.capture.live_capture.LiveCapture):
    """
    print output to screen if doesn't utilize files
    :args:
        capture:pyshark.capture.live_capture.LiveCapture - captured packages
    """
    for packet in capture:
        print(packet)


def get_data(interface:str="eth0", capture_filter:str=None, only_summaries:str=False, output_file:str=None,
             packet_count:int=10, timeout:int=10)->pyshark.capture.live_capture.LiveCapture:
    """
    Based on the interface get network insight
    :args:
        interface:str - interface option
        capture_filter:str - capturing filter (used for specific such as net-flow)
        only_summaries:bool - display packet summaries instead of the entire packet contents.
        output_file:str - file to write captured packets to, in addition to displaying them. For example, "captured.pcapng".
        packet_count:int - Amount of packets to add to the packet list (0 will go forever)
        timeout:int - sniff time
    :params:
        capture:pyshark.capture.live_capture.LiveCapture - captured packages
    :return:
        capture
    """
    # Sniff from interface
    capture = pyshark.LiveCapture(interface=interface, capture_filter=capture_filter, only_summaries=only_summaries,
                                  output_file=output_file)
    capture.sniff(packet_count=packet_count, timeout=timeout)

    return capture

def read_data(file_path:str=FILE_PATH)->bool:
    """
    Read content from pcap and store as CSV file
    :args:
        file_path:str - pcap file where content is stored
    :params:
        status:bool
        csv_file:str - file path for CSV data
    """
    status = True
    csv_file: str = file_path.replace("pcap", "csv")
    try:
        NFStreamer(source=file_path).to_csv(path=csv_file, columns_to_anonymize=())
    except Exception as error:
        status = False
        print(f"Failed Failed to convert content into CSV file (Error: {error})")

    return status


def write_data(file_path:str=FILE_PATH):
    """
    Write CVS file into JSON file
    :args:
        file_path:str - pcap file where content is stored
    :params:
        csv_file:str - file path for CSV file
        json_file:str - file path for JSON file
    """
    csv_file = file_path.replace("pcap", "csv")
    json_file = file_path.replace("pcap", "json")
    try:
        with open(json_file, 'w') as f:
            try:
                with open(csv_file) as csvf:
                    try:
                        csvReader = csv.DictReader(csvf)
                    except Exception as error:
                        print(f"Failed to read content from {csv_file} (Error: {error})")
                    else:
                        for row in csvReader:
                            try:
                                f.write(json.dumps(row) + "\n")
                            except Exception as error:
                                print(f"Failed to write line into {json_file} (Error: {error})")
            except Exception as error:
                print(f"Failed to open CSV file to be read (Error: {error})")
    except Exception as error:
        print(f"Failed to open JSON file to write content into (Error: {error})")


def main():
    """
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
    :params:
        capture_filter:str - capturing filter (used for specific such as net-flow)
        cap:pyshark.capture.file_capture.FileCapture - declaration for File Capture
        full_path:str - file path
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("interface", type=str, default="eth0", choices=__get_interfaces(), help="Interface to get data from")
    parser.add_argument("--timeout", type=int, default=1, help="Wait time")
    parser.add_argument("--packet-count", type=int, default=10, help="Amount of packets to add to the packet list (0 will go forever)")
    parser.add_argument("--file-path", type=str, default=FILE_PATH, help="PCAP file to initially store data in")
    parser.add_argument("--net-flow", type=bool, nargs='?', const=True, default=False, help="Get NetFlow data")
    parser.add_argument("--sflow", type=bool, nargs='?', const=True, default=False, help="Get sFlow data")
    parser.add_argument("--gemini-net", type=bool, nargs='?', const=True, default=False, help="Get Gemini-Net data")
    parser.add_argument("--generic-filter", type=str, default=None, help="manually declare a capturing filter")
    parser.add_argument("--only-summary", type=bool, nargs='?', const=True, default=False, help="Display packet summaries instead of the entire packet contents")
    parser.add_argument("--view-interfaces",  type=bool, nargs='?', const=True, default=False, help="get list of possible interfaces")
    args = parser.parse_args()

    if args.view_interfaces is True: # print list of interfaces
        for interface in __get_interfaces():
            print(interface)
        exit(1)

    capture_filter = None
    if args.net_flow is True:
        # capture filter to capture only NetFlow packets
        # sample shell command: sudo tcpdump -i eth0 udp port 2055 -w netflow.pcap
        capture_filter = "udp port 2055"
    elif args.sflow is True:
        # capture filter to capture only sFlow packets
        # sample shell command: sudo tcpdump -i eth0 udp port 6343 -w sflow.pcap
        capture_filter = "udp port 6343"
    elif args.gemini_net is True:
        # capture only Gemini-Net packets
        # sample shell command: sudo tcpdump -i eth0 udp port 1212 -w gemini-net.pcap
        capture_filter = "udp port 1212"
    elif args.generic_filter is not None:
        capture_filter = args.generic_filter

    cap, full_path = __create_file(file_path=args.file_path)
    capture = get_data(interface=args.interface, capture_filter=capture_filter, only_summaries=args.only_summary,
                       output_file=full_path, packet_count=args.packet_count, timeout=args.timeout)
    if full_path is not None:
        __close_file(cap=cap, file_path=args.file_path)
        if read_data(file_path=full_path):
            write_data(file_path=full_path)
    else:
        __print_packets(capture=capture)


if __name__ == '__main__':
    main()
