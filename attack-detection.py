"""

      This is an upgraded advance version of the original tool EclipseSH has created
      
      PPS Meter and DDOS Packet Capturing Tool
        - With Discord Notification Via Webhook API

@author: Erupt
@since: 3/24/22
"""
import os, time, subprocess, sys, time, datetime, requests, json
from datetime import datetime

clear = print("\033[2J\033[1;1H")
now = datetime.now()
current_time = now.strftime("%d-%m-%Y--%H:%M:%S")
webhook = ""

class Detection:
  def GetInterface():
    try:
      return subprocess.getoutput(f"ifconfig").split("\n")[0].split(":")[0]
    except:
      print("[x] Error, Something went wrong with grabbing the system's interface....")
      exit(0)
    
  def GetPPS():
    try:
      first_check = subprocess.getoutput(f"grep {Detection.GetInterface()}: /proc/net/dev | cut -d :  -f2 "+"| awk '{ print $2 }'")
      time.sleep(1)
      second_check = subprocess.getoutput(f"grep {Detection.GetInterface()}: /proc/net/dev | cut -d :  -f2 "+"| awk '{ print $2 }'")
      return int(str(int(first_check) - int(second_check)).replace("-", ""))
    except:
      print("[x] Error, Something went wrong with calculating packets for PPS")
      exit(0)

  def Attack_Detected(pps_detected, max_pps):
    os.system(f"tcpdump -n -s0 -c {pps_detected} -w /root/TCPDUMP/capture.{current_time}.pcap")
    Utils.message_hook(webhook)


class Utils:
  def message_hook(url):
    payload = {
          "embeds": [
        {
          "title": "DDoS Attack",
          "description": "DDoS attack had been Detected.",
          "url": "https://instagram.com/clipzy.v",
          "color": 16056320,
          "fields": [
            {
              "name": "Server:",
              "value": "``Skrillec VPN Canada``",
              "inline": True
            },
            {
              "name": "Dump Name",
              "value": f"``capture.{current_time}.pcap``",
              "inline": True
            },
            {
              "name": "PPS:",
              "value": f"``{Detection.GetPPS()}``",
              "inline": True
            }
          ],
          "author": {
            "name": "Skrillec VPN",
            "url": "https://instagram.com/clipzy.v",
            "icon_url": "https://cdn.discordapp.com/attachments/749377649683595378/763196139595628565/Certified-Ethical-Hacker.png"
          },
          "footer": {
            "text": "Our system has sucessfully captured an attack.",
            "icon_url": "https://cdn.discordapp.com/attachments/749377649683595378/763196139595628565/Certified-Ethical-Hacker.png"
          },
          "thumbnail": {
            "url": "https://cdn.discordapp.com/attachments/850908400153395220/853359270832635904/download.gif"
          }
        }
      ]
    }
    header_data = {'content-type': 'application/json'}
    requests.post(webhook, json.dumps(payload), headers=header_data)

clear
print("[+] PPS Meter Started....")
if len(sys.argv) < 2:
  print(f"[x] Error, Invalid argument\nUsage {sys.argv[0]} <max_pps>")
  exit(0)
max_pps = sys.argv[1]
while True:
  current_pps = Detection.GetPPS()
  print(f"\r                       ", end="")
  print(f"\rCurrent PPS: {current_pps}", end="")
  if current_pps > int(max_pps):
    Detection.Attack_Detected(webhook, current_pps)