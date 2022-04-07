### Using your own certificate and key

```sh
docker-compose down
sudo rm -rf ./data
mkdir -p ./data/step-ca/secrets

cp "$(mkcert -CAROOT)/rootCA.pem" ./data/step-ca/
cp "$(mkcert -CAROOT)/rootCA-key.pem" ./data/step-ca/
echo '123456' | tee "$PWD/data/step-ca/secrets/password"

sudo chown -R 1000:1000 "$PWD/data/step-ca"

docker run --rm -it -v "$PWD/data/step-ca:/home/step" smallstep/step-ca step ca init \
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
