#!/usr/bin/env python

import scapy.all as scapy
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target range to scan")
    options = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify a target ip range, use --help for more info.")
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    # scapy.ls(scapy.ARP())
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # scapy.ls(scapy.Ether())
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in answered_list:
        clients_list.append({"ip": element[1].psrc, "mac": element[1].hwsrc})
    return clients_list

def print_result(results_list):
    print(f"IP\t\t\tMAC Address\n------------------------------------------------------")
    for client in results_list:
        print(f"{client['ip']}\t\t{client['mac']}")

options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)