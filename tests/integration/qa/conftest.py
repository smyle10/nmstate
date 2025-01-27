import pytest
import subprocess


@pytest.fixture(scope="session", autouse=True)
def create_veth_pairs(count=5):
    ipv6_conf = "/proc/sys/net/ipv6/conf"
    for i in range(count):
        # check if VC-TEST{i} already exists
        if (
            f"VC-TEST{i}"
            in subprocess.run(
                f"ip link show VC-TEST{i}".split(), capture_output=True
            ).stdout.decode()
        ):
            continue

        mac_id = f"{i:02d}"
        subprocess.run(
            (
                f"ip link add VC-TEST{i} addr cc:cc:cc:cc:aa:{mac_id} type "
                f"veth peer name VC-TEST{i}_p addr cc:cc:cc:cc:bb:{mac_id}"
            ).split()
        )
        subprocess.run(f"ip link set VC-TEST{i} up".split())
        subprocess.run(f"ip link set VC-TEST{i}_p up".split())
        subprocess.run(f"nmcli dev set VC-TEST{i} managed yes".split())
        subprocess.run(f"nmcli dev set VC-TEST{i}_p managed yes".split())
        with open(f"{ipv6_conf}/VC-TEST{i}/disable_ipv6", "w") as f:
            f.write("1")
        with open(f"{ipv6_conf}/VC-TEST{i}_p/disable_ipv6", "w") as f:
            f.write("1")
