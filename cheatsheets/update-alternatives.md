# Update Alternatives Cheatsheet

## Add Alternative

```sh
sudo update-alternatives --install /usr/bin/java java /opt/java/java8/bin/java 100
#(1) (2)                 (3)       (4)           (5)  (6)                      (7)
```

1.  Root permissions are necessary
2.  The name of the command.  How could you have forgotten this already?
3.  This means that you are adding an alternative
4.  The location of the symlink that you will use to execute the alternative
5.  The name of the alternative
6.  The location of the actual executable
7.  The priority of the alternative

## Set Alternative To Be Used

```sh
sudo update-alternatives --config java
#(1) (2)                 (3)      (4)
```

1.  Root permissions are necessary
2.  The name of the command.  Try to keep up.
3.  This will present a list of installed alternatives for you to select
4.  The name of the alternative that you want to modify
