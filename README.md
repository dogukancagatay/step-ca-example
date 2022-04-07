# Setup step-ca

## Initialization from scratch

```sh
mkdir -p "$PWD/data/step-ca"
sudo chown -R 1000:1000 "$PWD/data/step-ca"
docker run --rm -it -v "$PWD/data/step-ca:/home/step" smallstep/step-ca step ca init
```

### Add your password

<!-- echo <your password here> > /home/step/secrets/password -->

```sh
echo <your password here> | sudo tee "$PWD/data/step-ca/secrets/password"
sudo chown -R 1000:1000 "$PWD/data/step-ca/secrets/password"
```

## Start your step-ca Instance

```sh
docker-compose up -d step-ca
```

Save your _Root fingerprint_ somewhere to use afterwards.

```
Generating root certificate...
all done!

Generating intermediate certificate...
all done!

✔ Root certificate: /home/step/certs/root_ca.crt
✔ Root private key: /home/step/secrets/root_ca_key
✔ Root fingerprint: f032205...
✔ Intermediate certificate: /home/step/certs/intermediate_ca.crt
✔ Intermediate private key: /home/step/secrets/intermediate_ca_key
✔ Database folder: /home/step/db
✔ Default configuration: /home/step/config/defaults.json
✔ Certificate Authority configuration: /home/step/config/ca.json

Your PKI is ready to go. To generate certificates for individual services see 'step help ca'.

FEEDBACK 😍 🍻
      The step utility is not instrumented for usage statistics. It does not
      phone home. But your feedback is extremely valuable. Any information you
      can provide regarding how you’re using `step` helps. Please send us a
      sentence or two, good or bad: feedback@smallstep.com or join
      https://github.com/smallstep/certificates/discussions.
```

Then, go to https://localhost:9000/health to make sure service is running.

## Enable ACME provisioner

```sh
docker-compose exec step-ca step ca provisioner add acme --type ACME
docker-compose restart
```

## Add CA to your development environment

```sh
step ca bootstrap --ca-url https://localhost:9000 --install --fingerprint <fingerprint-acquired>
step ca bootstrap --ca-url https://localhost:9000 --install --fingerprint f0322055102894cae067c9e23ed3139f670f39c54233a5012f2c723614868d58

```

This command setup created CA on your computer to be able to acquire certificates, and adds the CA to your computer's trust store.

Check if CA is added to your trust store.

```sh
curl https://localhost:9000/health
```

Create a sample certificate for localhost.

```sh
step ca certificate site.myhost.local site_home_local.crt site_home_local.key
```

### Run traefik first

```sh
docker-compose up -d traefik
sleep 10
docker-compose up -d whoami
```

## Initializing step-ca from your own CA certificate and key

```sh
docker-compose down
sudo rm -rf ./data
mkdir -p ./data/step-ca/secrets

cp "$(mkcert -CAROOT)/rootCA.pem" ./data/step-ca/
cp "$(mkcert -CAROOT)/rootCA-key.pem" ./data/step-ca/
echo '123456' | tee "$PWD/data/step-ca/secrets/password"

# don't chown on MacOS
sudo chown -R 1000:1000 "$PWD/data/step-ca"

docker-compose run step-ca step ca init \
--root "/home/step/rootCA.pem" \
--key "/home/step/rootCA-key.pem" \
--name "mkcert CA" \
--provisioner "admin" \
--dns "localhost,ca.internal,ca.myhost.local,acme.myhost.local" \
--address ":9000" \
--password-file=/home/step/secrets/password

docker-compose up -d step-ca
docker-compose exec step-ca step ca provisioner add acme --type ACME
docker-compose restart
docker-compose up -d traefik
docker-compose logs -f traefik
```

ref: https://smallstep.com/docs/tutorials/intermediate-ca-new-ca

## References

- https://hub.docker.com/r/smallstep/step-ca
- https://smallstep.com/docs/step-ca/installation
