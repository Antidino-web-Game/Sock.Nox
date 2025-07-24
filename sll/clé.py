from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime

# Générer une clé privée
key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# Créer un certificat auto-signé
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "FR"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Pays de la Loire"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Briosne-lès-Sables"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "MonServeur"),
    x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
])

cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer)\
    .public_key(key.public_key())\
    .serial_number(x509.random_serial_number())\
    .not_valid_before(datetime.datetime.utcnow())\
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))\
    .sign(key, hashes.SHA256())

# Sauvegarder la clé et le certificat
with open("key.pem", "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

with open("cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))