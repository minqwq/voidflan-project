class cpu:
    def get_cpu_model():
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if line.startswith("model name"):
                        return line.split(":", 1)[1].strip()
            return "Failed to Fetch"
        except FileNotFoundError:
            print("/proc/cpuinfo was not found")
        except Exception as e:
            print(e)

    def get_cpu_flags():
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if line.startswith("flags"):
                        return line.split(":", 1)[1].strip()
            return "Failed to Fetch"
        except FileNotFoundError:
            print("/proc/cpuinfo was not found")
        except Exception as e:
            print(e)
