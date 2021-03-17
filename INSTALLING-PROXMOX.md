# Installing Proxmox

### Reboot into Hetzner Rescue System

Using the [Hetzner Robot](https://robot.your-server.de/server), navigate to your server and the _'Rescue'_ tab.

Choose Linux, 64-bit and select your SSH public key so that you can login over SSH and install the system through that.
You can add extra public keys through the [Key management page](https://robot.your-server.de/key/index).

Then click _'Activate Rescue System'_. The next time you reboot, the system will reboot to to the Hetzner Rescue System. You can do that by clicking the _'Reset'_ tab and choosing _'Execute an automatic hardware reset'_ and clicking _'Send'_.

### Install Proxmox with installimage

SSH into your servers Rescue System and start the installimage application:

```bash
~# ssh root@<my-server-ip>
~# installimage
```

Choose an OS to install - I chose _'Other/Proxmox-Virtualization-Environment-On-Debian-Buster'_.

Once the installimage config script is open, you need to configure a few things.

#### Enter hostname

This needs to be a FQDN, e.g. `HOSTNAME host.yourdomain.com`

#### Configure RAID

- If you have two equally sized drives in your machine, the default will be Software RAID 1 / Mirroring (`SWRAIDLEVEL 1`). Your drives will be mirrored which will provide some kind of way out should one of them fail. However you will only be able to use 50% of your total storage space.
- You could also choose Software RAID 0 / Striping (`SWRAIDLEVEL 0`). This will pool your drives so you will have twice the storage capacity you would if you used RAID 1, but the downside is if either of the drives fail, you will probably lose all of your data. Depending on the specification of your server, and the reliability of modern SSDs, and your confidence in your backups you might consider this a risk worth taking. There may also be some small performance benefit.
- You can turn off RAID entirely by setting `SWRAID 0`. If you do this, Proxmox will be installed on your first drive and your second drive will be unused.
- More comprehensive information about other RAID levels and about recovering the RAID array is here: https://community.hetzner.com/tutorials/howto-setup-mdadm

#### Verify storage details

The defaults for storage definitions were fine for my use case.

A 512M Boot partition, and then a LVM partition that takes up the rest of the disk.
Then a 15G Logical Volume to act as the root partition for the Proxmox installation, and a 6GB swap partition.

We will use the rest of the space to create a LVM Thin Pool which we will initialise in the next section. This [Thin Provisioning](https://www.theurbanpenguin.com/thin-provisioning-lvm2/) will allow us to make optimal use of our storage space.

```text
PART  /boot  ext3  512M
PART  lvm    vg0    all

LV  vg0  root  /     ext3  15G
LV  vg0  swap  swap  swap   6G
```

#### Reboot

Press **F2** to save, then **F10** to exit.

You should see a message somewhat like:

````text
Your server will be installed now, this will take some minutes
You can abort at any time with CTRL+C ...```
````

The install and update process will take around 10 minutes or so. Once it has completed, you should see this message:

```text
                  INSTALLATION COMPLETE
   You can now reboot and log in to your new system with the
 same credentials that you used to log into the rescue system.
```

# Accessing the new Proxmox instance

## By HTTP

The Proxmox web interface will be running now on _https://your-server-ip:8006_, but if you try to access it you will get security warnings as the TLS certificate has not yet been set up.

If you bypass these you will be able to access the Web UI, but I'd recommend to set up TLS as it's so easy nowadays with LetsEncrypt / ACME.

## By SSH

Check that you can SSH into your freshly installed Proxmox machine:

`~# ssh root@<your-server-ip>`

You will probably get a warning like:

```text
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@     WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!    @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
...
```

This is just because the .ssh keys have changed on the server when it rebooted from Rescue Mode into the ProxMox installation.

Run `~# ssh-keygen -R <your-server-ip>` to remove the offending key and then try SSHing again.

```text
~# ssh root@<your-server-ip>
Linux Proxmox-VE 5.4.44-2-pve #1 SMP PVE 5.4.44-2 (Wed, 01 Jul 2020 16:37:57 +0200) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Mon Jul 13 16:44:41 2020 from 176.250.88.220
root@Proxmox-VE ~ #
```

Now you are logged in as root, you should set your root password as you will need it later:

```text
root@Proxmox-VE ~ # passwd
New password:
Retype new password:
passwd: password updated successfully
```

Now continue onto [Configuring Proxmox](README.md) to configure the system with a dialog-based setup script similar to the Hetzner installimage script.