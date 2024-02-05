import winreg
import subprocess

def detect_antivirus():
    # List of antivirus programs to detect
    antivirus_list = [
        "Avast",
        "Windows Defender",
        "Trend Micro",
        "Bitdefender",
        "Kaspersky",
        "ESET",
        "AVG",
        "McAfee",
    ]

    detected_antiviruses = []

    for antivirus in antivirus_list:
        if is_installed(antivirus):
            detected_antiviruses.append(antivirus)

    return detected_antiviruses

def is_installed(antivirus):
    try:
        if antivirus == "Windows Defender":
            # Check if the "WinDefend" service is running
            output = subprocess.check_output(["sc", "query", "WinDefend"]).decode("utf-8")
            if "RUNNING" in output:
                return True
            else:
                return False
        else:
            # Check registry entries to detect the presence of other antivirus programs
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
            hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)

            for i in range(winreg.QueryInfoKey(hkey)[0]):
                subkey_name = winreg.EnumKey(hkey, i)
                subkey_path = f"{key_path}\\{subkey_name}"
                
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path) as subkey:
                        display_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                        if display_name and antivirus.lower() in display_name.lower():
                            return True
                except Exception as e:
                    pass

            return False

    except Exception as e:
        # Handle exceptions, print the error, and return False
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    # Detect antivirus programs and print the results
    detected_antiviruses = detect_antivirus()

    if len(detected_antiviruses) >= 2:
        print("At least 2 different antivirus programs detected on the system.")
        print("Detected Anti-Virus Software:")
        for antivirus in detected_antiviruses:
            print(antivirus)
    else:
        print("Less than 2 antivirus programs detected on the system.")
        if detected_antiviruses:
            print("Detected Anti-Virus Software:")
            for antivirus in detected_antiviruses:
                print(antivirus)
        else:
            print("No antivirus software detected.")