# SSH Cheatsheet

## Password-less Logins - Using Utilities

1\. Generate a public & private key pair

```sh
ssh-keygen
```

1\. Add the generated public key to the remote host's `~/.ssh/authorized_keys` file

```sh
ssh-copy-id eviljoe@remote-host
```


## Password-less Logins - Manual

1\. Generate a public & private key pair

```sh
ssh-keygen
```

2\. Copy the generated public key (in `~/.ssh/id_rsa.pub`) to your clipboard

```sh
cat ~/.ssh/id_rsa.pub
```

3\. Login to the remote host

```sh
ssh eviljoe@remote-host
```

4\. Append the private key to the `~/.ssh/authorized_keys` file

```sh
vim ~/.ssh/authorized_keys
```
