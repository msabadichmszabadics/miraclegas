import subprocess

def allow_firewall_rule(rule_name):
    try:
        # Allow the specified firewall rule for inbound traffic
        subprocess.run(["netsh", "advfirewall", "firewall", "set", "rule", "name=" + rule_name, "new", "enable=yes"])

        # Allow the specified firewall rule for outbound traffic
        subprocess.run(["netsh", "advfirewall", "firewall", "set", "rule", "name=" + rule_name, "new", "enable=yes", "direction=out"])

        print(f"Firewall rule '{rule_name}' allowed for both inbound and outbound traffic.")
    except subprocess.CalledProcessError as e:
        print(f"Error while allowing firewall rule '{rule_name}': {e}")

if __name__ == "__main__":
    rule_name = "#rickconf"  # Replace with the name of your firewall rule
    allow_firewall_rule(rule_name)
