# Mount Cheatsheet

## Mount Windows Drive

```sh
sudo mount --read-only /dev/sdb2 /media/win-hdd
#(1) (2)   (3)         (4)      (5)
```

1.  Root permissions are necessary
2.  The name of the command.  It mounts stuff.  That's what this guide is about.
3.  If you are mounting a Windows drive, you will probably have to mount as read-only.  This is because windows doesn't
    really shut down.  It just hibernates.  When Windows is hibernating it puts the drive in a state where it can't be
    accessed my multiple clients with write permissions.
4.  The reference to the drive that is to be mounted.
5.  The mount point.  The place that you will go to access the contents of the drive.
