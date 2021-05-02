# py-init

A small python based initialization tool to kickstart Raspberry Pi configuration.

The main aim for this tool is to automate configuration steps that I usually take, everytime I set up a new Raspberry Pi. I hope it helps you too.

## manual

This tool needs python3 installed.

1. Clone this repository
2. Change the settings you need in the [config.json](config.json), remove the settings you don't want to edit from it. (In case you screw up, there is a copy under [config.json.default](config.json.default))
3. Run the tool using the following command
   ```bash
   sudo ./configure
   ```

## configuration settings

[config.json](config.json)

```json
{
  "hostname": "newhostname",
  "swap_mb": 1024,
  "expand_fs": true,
  "wifi_settings": {
    "country": "CH",
    "ssid": "mywifiname",
    "psk": "mywifipassword"
  },
  "network_config": [
    {
      "interface": "eth0",
      "ip_address": "192.168.1.105/24",
      "routers": "192.168.1.1",
      "domain_name_servers": ["8.8.8.8", "8.8.4.4"]
    },
    {
      "interface": "wlan0",
      "ip_address": "192.168.1.106/24",
      "routers": "192.168.1.1",
      "domain_name_servers": ["8.8.8.8", "8.8.4.4"]
    }
  ],
  "set_locale_en_us": true,
  "reduce_journald_size": true,
  "new_user_password": "newpassword",
  "disable_password_login": false,
  "update_packages": true
}
```

---

### hostname

type: string

New hostname to set.

---

### swap_mb

type: int

Change size of swap (default: 100).

---

### expand_fs

type: bool

Expand root filesystem `/`.

---

### wifi_settings

| value   | type   |
| ------- | ------ |
| country | string |
| ssid    | string |
| psk     | string |

Configuring the wifi of your Raspberry Pi.

- For the right value of `country` find the correct alpha-2 code [here](https://en.wikipedia.org/wiki/ISO_3166-1).

---

### network_config

| value               | type         |
| ------------------- | ------------ |
| interface           | string       |
| ip_address          | string       |
| routers             | string       |
| domain_name_servers | List[string] |

Configuring static IP addresses on your Raspberry Pi.

- For the right value of `interface` see `ifconfig`-command.
- Write `ip_address`in CIDR-format including subnet information.

---

### set_locale_en_us

type: bool

Setting the locale settings to en_us (default: en_gb)

---

### reduce_journald_size

type: bool

Configuring journald to only use 50MB of storage.

---

### new_password

type: str

Changing the password of the `pi`user.

---

### disable_password_login

type: bool

Disabling the password login for the `pi`user. Only possible if `/home/pi/.ssh/authorized_keys`file exists and is not empty. Does overwrite the `new_password` parameter.

---

### update_packages

type: bool

Updates all the packages installed after reboot. This copies a script to `/home/pi/temp/updating`and runs it using the `/etc/rc.local` after the first reboot.

---

## By me a coffee if you like this tool

<a href="https://www.buymeacoffee.com/remohoeppli" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;" ></a>
