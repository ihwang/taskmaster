

raw_yaml = {"program": {"sleep": {"cmd": "sleep 5", "cmd_amt": 3}}}

for key, value in raw_yaml["program"].items():
    print(value["foo"])