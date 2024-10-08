import os
import time
import subprocess

def start_rtl_power(csv_filename):
    command = f"rtl_power -f 446.300M:446.600M:1k -i 5s {csv_filename}"
    process = subprocess.Popen(command, shell=True)
    return process

def read_last_line(csv_filename):
    try:
        with open(csv_filename, 'r') as file:
            lines = file.readlines()
            if lines:
                return lines[-1]
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Hata: {e}")
    return None

def rtl_output(csv_filename):
    power = None
    while True:
        try:
            last_line = read_last_line(csv_filename)
            if last_line:
                parts = last_line.strip().split(',')
                try:
                    powerdb = float(parts[262].replace(' dbm', ''))
                    if power is None or powerdb > power:
                        power = powerdb
                        data = {'power': power}
                        print(f"Yeni güç değeri: {data}")
                except (IndexError, ValueError) as e:
                    print(f"Veri işleme hatası: {e}")
                    continue

            time.sleep(1)

        except Exception as e:
            print(f"Beklenmeyen hata: {e}. 5 saniye sonra tekrar denenecek...")
            time.sleep(5)

if __name__ == "__main__":
    while True:
        try:
            script_dir = os.path.dirname(os.path.realpath(__file__))
            csv_filename = os.path.join(script_dir, "output.csv")
            rtl_power_process = start_rtl_power(csv_filename)
            try:
                rtl_output(csv_filename)
            except KeyboardInterrupt:
                rtl_power_process.terminate()
                print("\nrtl_power durduruldu.")
                break

        except Exception as e:
            print(f"Başlatma hatası: {e}. 5 saniye sonra tekrar başlatılacak...")
            time.sleep(5)
