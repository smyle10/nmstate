import distro
from packaging import version

def get_rhel_version():
    return distro.version()

# Check if the current RHEL version meets the specified criteria.
# similar to `rlIsRHEL` in beakerlib
def rl_is_rhel(operator: str, ver: str) -> bool:
    current_ver = version.parse(get_rhel_version())
    compared_ver = version.parse(ver)
    operators_map = {
        '>': current_ver.__gt__,
        '<': current_ver.__lt__,
        '>=': current_ver.__ge__,
        '<=': current_ver.__le__,
        '==': current_ver.__eq__,
        '=': current_ver.__eq__
    }
    return operators_map[operator](compared_ver)
