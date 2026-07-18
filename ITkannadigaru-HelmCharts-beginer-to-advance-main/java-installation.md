```
#!/bin/bash
sudo apt update
sudo apt install openjdk-17-jdk -y
```

```
java -version
```

```
update-java-alternatives --list
```

```
sudo update-alternatives --install /usr/bin/java java /usr/lib/jvm/java-17-openjdk-amd64/bin/java 1
sudo update-alternatives --install /usr/bin/javac javac /usr/lib/jvm/java-17-openjdk-amd64/bin/javac 1
sudo update-alternatives --config java
sudo update-alternatives --config javac
```