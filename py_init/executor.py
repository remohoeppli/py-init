from py_init.config_parser import Init_Configuration
import sys
from typing import Callable
from py_init.output.output import Output
import py_init.toolbox as toolbox


class Executor:
    def __init__(self, config: Init_Configuration):
        self.__output = Output()
        self.__config = config

    def __init_message(self) -> None:
        self.__output.info("py-init configuration script")

    def __reboot_message(self) -> None:
        self.__output.passed("installation complete")
        self.__output.info("please reboot the pi")

    def __execute(self, task: str, execution: Callable[[], None]) -> None:
        try:
            self.__output.started(task)
            execution()
            self.__output.passed(task)
        except Exception as e:
            self.__output.failed(task)
            self.__output.info(str(e))
            sys.exit()

    def __set_hostname(self) -> None:
        new_hostname = str(self.__config.hostname)
        old_hostname = toolbox.read_from_file("/etc/hostname")
        old_hostname = old_hostname.replace("\n", "").replace("\r", "")
        toolbox.write_to_file("/etc/hostname", new_hostname)
        toolbox.replace_string_in_file("/etc/hosts", old_hostname, new_hostname)

    def __set_swap_size(self) -> None:
        toolbox.copy_file("templates/dphys-swapfile", "/etc/dphys-swapfile")
        toolbox.replace_string_in_file(
            "/etc/dphys-swapfile",
            "CONF_SWAPSIZE=100",
            "CONF_SWAPSIZE=" + str(self.__config.swap_mb),
        )

    def __expand_rootfs(self) -> None:
        toolbox.call_bash_command("raspi-config --expand-rootfs > /dev/null 2>&1")

    def __set_wifi_settings(self) -> None:
        toolbox.copy_file(
            "templates/wpa_supplicant.conf", "/etc/wpa_supplicant/wpa_supplicant.conf"
        )
        if self.__config.wifi_settings:
            toolbox.replace_string_in_file(
                "/etc/wpa_supplicant/wpa_supplicant.conf",
                "WLAN_country_code",
                str(self.__config.wifi_settings.country),
            )
            toolbox.replace_string_in_file(
                "/etc/wpa_supplicant/wpa_supplicant.conf",
                "WLAN-SSID",
                str(self.__config.wifi_settings.ssid),
            )
            toolbox.replace_string_in_file(
                "/etc/wpa_supplicant/wpa_supplicant.conf",
                "WLAN-PASSWORT",
                str(self.__config.wifi_settings.psk),
            )
            toolbox.call_bash_command("rfkill unblock 0")

    def __set_network_settings(self) -> None:
        toolbox.copy_file("templates/dhcpcd.conf", "/etc/dhcpcd.conf")
        for network_config in self.__config.network_config:
            toolbox.append_to_file(
                "/etc/dhcpcd.conf", f"interface {network_config.interface}"
            )
            toolbox.append_to_file(
                "/etc/dhcpcd.conf", f"static ip_address={network_config.ip_address}"
            )
            toolbox.append_to_file(
                "/etc/dhcpcd.conf", f"static routers={network_config.routers}"
            )
            toolbox.append_to_file(
                "/etc/dhcpcd.conf",
                f"static domain_name_servers={' '.join(network_config.domain_name_servers)}",
            )
            toolbox.append_to_file("/etc/dhcpcd.conf", "")

    def __set_locale_en_us(self) -> None:
        toolbox.copy_file("templates/locale.gen", "/etc/locale.gen")
        toolbox.copy_file("templates/locale", "/etc/default/locale")
        toolbox.call_bash_command("dpkg-reconfigure -f noninteractive locales")
        toolbox.check_and_append_to_file("/home/pi/.bashrc", "export LC_ALL=C")

    def __reduce_journald_size(self) -> None:
        toolbox.copy_file(
            "templates/journald.conf",
            "/etc/systemd/journald.conf",
        )

    def __change_password(self) -> None:
        toolbox.call_bash_command(
            f"echo 'pi:{self.__config.new_user_password}' | chpasswd"
        )

    def __disable_password_login(self) -> None:
        toolbox.call_bash_command("passwd -l pi")

    def __prepare_update_packages_script(self) -> None:
        toolbox.call_bash_command("mkdir -p /home/pi/temp")
        toolbox.copy_file("templates/updating", "/home/pi/temp/updating")
        if not toolbox.check_string_in_file("/etc/rc.local", "/home/pi/temp/updating"):
            toolbox.replace_string_in_file(
                "/etc/rc.local", "exit 0", "/home/pi/temp/updating"
            )
            toolbox.append_to_file("/etc/rc.local", "exit 0")

    def install(self) -> None:
        self.__init_message()

        if self.__config.hostname:
            self.__execute("settings hostname", self.__set_hostname)

        if self.__config.swap_mb:
            self.__execute("setting swap size", self.__set_swap_size)

        if self.__config.expand_fs:
            self.__execute("expanding root fs", self.__expand_rootfs)

        if self.__config.wifi_settings:
            if (
                self.__config.wifi_settings.country
                and self.__config.wifi_settings.ssid
                and self.__config.wifi_settings.psk
            ):
                self.__execute("setting up wifi", self.__set_wifi_settings)
            else:
                self.__output.failed("setting up wifi")
                self.__output.info("invalid wifi settings, skipping")

        if len(self.__config.network_config):
            if (
                self.__config.network_config[0].interface
                and self.__config.network_config[0].ip_address
                and self.__config.network_config[0].routers
                and len(self.__config.network_config[0].domain_name_servers)
            ):
                self.__execute("setting up network config", self.__set_network_settings)
            else:
                self.__output.failed("setting up network config")
                self.__output.info("invalid network config, skipping")

        if self.__config.set_locale_en_us:
            self.__execute("setting locale en_us", self.__set_locale_en_us)

        if self.__config.reduce_journald_size:
            self.__execute("reduce journald size", self.__reduce_journald_size)

        if self.__config.new_user_password:
            self.__execute("changing password for pi", self.__change_password)

        if self.__config.disable_password_login:
            authorized_keys = "/home/pi/.ssh/authorized_keys"
            if toolbox.file_exists(authorized_keys) and toolbox.get_file_size(
                authorized_keys
            ):
                self.__execute(
                    "disabling password logins with pi", self.__disable_password_login
                )
            else:
                self.__output.failed("disabling password logins with pi")
                self.__output.info("no or empty outhorized key file, skipping")

        if self.__config.update_packages:
            self.__execute(
                "preparing packages update", self.__prepare_update_packages_script
            )
            self.__output.info("updating packages after reboot")

        self.__reboot_message()
