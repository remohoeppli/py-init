import json
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Network_Configuration:
    interface: Optional[str] = None
    ip_address: Optional[str] = None
    routers: Optional[str] = None
    domain_name_servers: List[str] = field(default_factory=list)


@dataclass
class Wifi_Settings:
    country: Optional[str] = None
    ssid: Optional[str] = None
    psk: Optional[str] = None


@dataclass
class Init_Configuration:
    hostname: Optional[str] = None
    swap_mb: Optional[int] = None
    expand_fs: bool = False
    wifi_settings: Optional[Wifi_Settings] = None
    network_config: List[Network_Configuration] = field(default_factory=list)
    set_locale_en_us: bool = False
    reduce_journald_size: bool = False
    new_user_password: Optional[str] = None
    disable_password_login: bool = False
    update_packages: bool = False


def read_config() -> Init_Configuration:
    config = Init_Configuration()

    with open("config.json", "r") as config_json:
        config_file = json.load(config_json)

    # hostname
    config.hostname = (
        str(config_file["hostname"]) if "hostname" in config_file else config.hostname
    )

    # swap_mb
    config.swap_mb = (
        int(config_file["swap_mb"]) if "swap_mb" in config_file else config.swap_mb
    )

    # expand_fs
    config.expand_fs = (
        bool(config_file["expand_fs"])
        if "expand_fs" in config_file
        else config.expand_fs
    )

    # wifi_settings
    if "wifi_settings" in config_file:
        config.wifi_settings = Wifi_Settings()
        config.wifi_settings.country = (
            config_file["wifi_settings"]["country"]
            if "country" in config_file["wifi_settings"]
            else config.wifi_settings.country
        )
        config.wifi_settings.ssid = (
            config_file["wifi_settings"]["ssid"]
            if "ssid" in config_file["wifi_settings"]
            else config.wifi_settings.ssid
        )
        config.wifi_settings.psk = (
            config_file["wifi_settings"]["psk"]
            if "psk" in config_file["wifi_settings"]
            else config.wifi_settings.psk
        )

    # network_config
    if "network_config" in config_file:
        for network_config_file in config_file["network_config"]:
            temp_net_conf = Network_Configuration()
            temp_net_conf.interface = (
                network_config_file["interface"]
                if "interface" in network_config_file
                else temp_net_conf.interface
            )
            temp_net_conf.ip_address = (
                network_config_file["ip_address"]
                if "ip_address" in network_config_file
                else temp_net_conf.ip_address
            )
            temp_net_conf.routers = (
                network_config_file["routers"]
                if "routers" in network_config_file
                else temp_net_conf.routers
            )
            temp_net_conf.domain_name_servers = (
                network_config_file["domain_name_servers"]
                if "domain_name_servers" in network_config_file
                else temp_net_conf.domain_name_servers
            )
            config.network_config.append(temp_net_conf)

    # set_locale_en_us
    config.set_locale_en_us = (
        bool(config_file["set_locale_en_us"])
        if "set_locale_en_us" in config_file
        else config.set_locale_en_us
    )

    # reduce_journald_size
    config.reduce_journald_size = (
        bool(config_file["reduce_journald_size"])
        if "reduce_journald_size" in config_file
        else config.reduce_journald_size
    )

    # new_user_password
    config.new_user_password = (
        str(config_file["new_user_password"])
        if "new_user_password" in config_file
        else config.new_user_password
    )

    # disable_password_login
    config.disable_password_login = (
        bool(config_file["disable_password_login"])
        if "disable_password_login" in config_file
        else config.disable_password_login
    )

    # update_packages
    config.update_packages = (
        bool(config_file["update_packages"])
        if "update_packages" in config_file
        else config.update_packages
    )

    return config
