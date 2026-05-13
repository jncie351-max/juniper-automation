from netmiko import ConnectHandler  # Import Netmiko for SSH device handling

# --- Device credentials and IP range ---
USER, PASS = "root", "root123"
DEVICES = [f"10.200.51.{i}" for i in range(1, 21)]  # Generates IPs .1 through .20

# --- The Junos commands to push ---
SET    = "set system login user jncie class super-user authentication encrypted-password $6$hDJ/3LqH$zpn5a.ErG9R1pxZh9x8xbIjv9k00VMJN/qRTQcKP4AlG2P1pYmAGxasSagDxO6BgZY56eVozi39oEMUlVShJG0"
COMMIT = "commit and-quit"  # Commits and exits config mode in one step

# --- Loop through each device and send the command ---
for ip in DEVICES:
    try:
        # Build the device dictionary Netmiko uses to establish the SSH session
        device = {"device_type": "juniper_junos", "host": ip, "username": USER, "password": PASS}

        with ConnectHandler(**device) as conn:           # Open SSH connection (auto-closes after block)
            output = conn.send_config_set([SET, COMMIT]) # Send set command then commit and-quit together
            print(f"[{ip}] SUCCESS:\n{output}")          # Print the router's response
            conn.disconnect()                            # Explicitly send clean SSH teardown before moving on
            print(f"[{ip}] Connection closed.\n")        # Confirm closure in output before next iteration

    except Exception as e:
        print(f"[{ip}] FAILED: {e}")                    # Catch connection/auth/timeout errors gracefully
