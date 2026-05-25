https://michael-simons.github.io/neo4j-migrations/2.2.2/

## Install

```sh
apt-get update
apt-get install curl
curl -LO https://github.com/michael-simons/neo4j-migrations/releases/download/2.2.2/neo4j-migrations-2.2.2-linux-x86_64.zip
apt-get install unzip
unzip neo4j-migrations-2.2.2-linux-x86_64.zip -d neo4j-migrations-dir
apt remove unzip
rm neo4j-migrations-2.2.2-linux-x86_64.zip
mv neo4j-migrations-dir/neo4j-migrations-2.2.2-linux-x86_64/bin/neo4j-migrations /bin/neo4j-migrations
rm -rf neo4j-migrations-dir
```

## Migrate

Run from this `neo4j/` directory:

```sh
neo4j-migrations --password:file ./password.txt -d recommender --location=file://$(pwd)/migrations -v migrate
```