import pytest
from fastapi.testclient import TestClient

from main import app, hitung_subnet

client = TestClient(app)

# (ip, prefix, mask, network, broadcast, first_host, last_host, usable_hosts)
KASUS_SUBNET = [
    pytest.param("172.16.5.130", 25, "255.255.255.128", "172.16.5.128", "172.16.5.255", "172.16.5.129", "172.16.5.254", 126, id="T01"),
    pytest.param("10.0.0.0", 30, "255.255.255.252", "10.0.0.0", "10.0.0.3", "10.0.0.1", "10.0.0.2", 2, id="T02"),
    pytest.param("192.168.1.0", 31, "255.255.255.254", "192.168.1.0", None, "192.168.1.0", "192.168.1.1", 2, id="T03"),
    pytest.param("192.168.1.5", 32, "255.255.255.255", "192.168.1.5", None, "192.168.1.5", "192.168.1.5", 1, id="T04"),
    pytest.param("192.168.1.10", 24, "255.255.255.0", "192.168.1.0", "192.168.1.255", "192.168.1.1", "192.168.1.254", 254, id="T05"),
    pytest.param("192.168.1.100", 26, "255.255.255.192", "192.168.1.64", "192.168.1.127", "192.168.1.65", "192.168.1.126", 62, id="T06"),
    pytest.param("172.16.50.1", 20, "255.255.240.0", "172.16.48.0", "172.16.63.255", "172.16.48.1", "172.16.63.254", 4094, id="T07"),
    pytest.param("10.0.0.5", 8, "255.0.0.0", "10.0.0.0", "10.255.255.255", "10.0.0.1", "10.255.255.254", 16777214, id="T08"),
    pytest.param("192.168.1.255", 24, "255.255.255.0", "192.168.1.0", "192.168.1.255", "192.168.1.1", "192.168.1.254", 254, id="T09"),
    pytest.param("0.0.0.0", 0, "0.0.0.0", "0.0.0.0", "255.255.255.255", "0.0.0.1", "255.255.255.254", 4294967294, id="T10"),
]

KASUS_INVALID = [
    pytest.param("256.1.1.1", 24, id="X01-oktet-lebih-255"),
    pytest.param("192.168.01.1", 24, id="X02-nol-di-depan"),
    pytest.param("192.168.1", 24, id="X03-oktet-kurang"),
    pytest.param("192.168.1.1.1", 24, id="X04-oktet-berlebih"),
    pytest.param("abc", 24, id="X05-bukan-ip"),
    pytest.param("", 24, id="X06-ip-kosong"),
    pytest.param("192.168.1.1", 33, id="X07-prefix-33"),
    pytest.param("192.168.1.1", -1, id="X08-prefix-negatif"),
    pytest.param("192.168.1.1", "abc", id="X09-prefix-bukan-angka"),
    pytest.param("192.168.1.1", 24.5, id="X10-prefix-desimal"),
    pytest.param(" 192.168.1.1", 24, id="X11-ada-spasi"),
    pytest.param("192.168.1.1", "", id="X12-prefix-kosong"),
]


@pytest.mark.parametrize(
    "ip, prefix, mask, network, broadcast, first_host, last_host, usable",
    KASUS_SUBNET,
)
def test_hitung_subnet_sukses(ip, prefix, mask, network, broadcast, first_host, last_host, usable):
    harapan = {
        "mask": mask,
        "network": network,
        "broadcast": broadcast,
        "first_host": first_host,
        "last_host": last_host,
        "usable_hosts": usable,
    }
    assert hitung_subnet(ip, prefix) == harapan


@pytest.mark.parametrize("ip, prefix", KASUS_INVALID)
def test_hitung_subnet_ditolak(ip, prefix):
    with pytest.raises(ValueError):
        hitung_subnet(ip, prefix)


def test_api_subnet_sukses_a01():
    r = client.get("/api/subnet", params={"ip": "172.16.5.130", "prefix": "25"})
    assert r.status_code == 200
    assert r.json() == {
        "mask": "255.255.255.128",
        "network": "172.16.5.128",
        "broadcast": "172.16.5.255",
        "first_host": "172.16.5.129",
        "last_host": "172.16.5.254",
        "usable_hosts": 126,
    }


def test_api_subnet_slash31_a02():
    r = client.get("/api/subnet", params={"ip": "192.168.1.0", "prefix": "31"})
    assert r.status_code == 200
    data = r.json()
    assert data["broadcast"] is None
    assert data["usable_hosts"] == 2


@pytest.mark.parametrize(
    "params",
    [
        pytest.param({"ip": "256.1.1.1", "prefix": "24"}, id="A03-oktet-256"),
        pytest.param({"ip": "192.168.01.1", "prefix": "24"}, id="A04-nol-di-depan"),
        pytest.param({"ip": "192.168.1.1", "prefix": "abc"}, id="A05-prefix-abc"),
        pytest.param({"ip": "192.168.1.1"}, id="A06-prefix-hilang"),
    ],
)
def test_api_subnet_input_tidak_valid(params):
    r = client.get("/api/subnet", params=params)
    assert r.status_code == 400
    assert "detail" in r.json()


def test_api_halaman_utama_a10():
    r = client.get("/")
    assert r.status_code == 200
    assert "<html" in r.text.lower()