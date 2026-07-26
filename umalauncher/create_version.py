import pyinstaller_versionfile
import version


def _numeric_version():
    """pyinstaller_versionfile requires a digits-only dotted version for the
    Windows PE resource. version.VERSION may carry a '-modN' suffix (e.g.
    '1.18.6-mod1'), which version.parse_version normalises to a numeric tuple
    (1, 18, 6, 1) -> '1.18.6.1'."""
    return version.vstr(version.parse_version(version.VERSION))


def generate():
    numeric_version = _numeric_version()
    pyinstaller_versionfile.create_versionfile(
        output_file="version.rc",
        version=numeric_version,
        file_description="Uma Launcher",
        internal_name="Uma Launcher",
        original_filename="UmaLauncher.exe",
        product_name="Uma Launcher"
    )
    # Global release
    pyinstaller_versionfile.create_versionfile(
        output_file="version_global.rc",
        version=numeric_version,
        file_description="Uma Launcher (Global)",
        internal_name="Uma Launcher (Global)",
        original_filename="UmaLauncher-Global.exe",
        product_name="Uma Launcher (Global)"
    )
    # Steam JP release
    pyinstaller_versionfile.create_versionfile(
        output_file="version_jp_steam.rc",
        version=numeric_version,
        file_description="Uma Launcher (Steam)",
        internal_name="Uma Launcher (Steam)",
        original_filename="UmaLauncher-Steam.exe",
        product_name="Uma Launcher (Steam)"
    )

if __name__ == "__main__":
    generate()
