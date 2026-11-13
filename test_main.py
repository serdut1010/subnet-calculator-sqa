from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)

def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

@pytest.mark.parametrize(
    "ip,prefix,expected_net,expected_broadcast,expected_hosts,expected_first,expected_last,expected_mask",
    [
        ("172.16.5.130", 25, "172.16.5.128", "172.16.5.255", 126, "172.16.5.129", "172.16.5.254", "255.255.255.128"),
        ("10.0.0.0", 30, "10.0.0.0", "10.0.0.3", 2, "10.0.0.1", "10.0.0.2", "255.255.255.252"),
        ("192.168.1.0", 31, "192.168.1.0", None, 2, "192.168.1.0", "192.168.1.1", "255.255.255.255"),
        ("192.168.1.5", 32, "192.168.1.5", None, 1, "192.168.1.5", "192.168.1.5", "255.255.255.255"),
    ]
)
def test_hitung_subnet_success(ip, prefix, expected_net, expected_broadcast, expected_hosts, expected_first, expected_last, expected_mask):
    response = client.get(f"/api/subnet?ip={ip}&prefix={prefix}")
    assert response.status_code == 200
    data = response.json()
    assert data["network"] == expected_net
    assert data["broadcast"] == expected_broadcast
    assert data["usable_hosts"] == expected_hosts
    assert data["first_host"] == expected_first
    assert data["last_host"] == expected_last
    assert data["mask"] == expected_mask

@pytest.mark.parametrize(
    "ip,prefix",
    [
        ("256.1.1.1", 24),
        ("192.168.01.1", 24),
        ("192.168.1", 24),
        ("abc", 24),
        ("", 24),
        ("192.168.1.1", 33),
        ("192.168.1.1", -1),
    ]
)
def test_hitung_subnet_invalid(ip, prefix):
    response = client.get(f"/api/subnet?ip={ip}&prefix={prefix}")
    assert response.status_code == 400
    assert "detail" in response.json()

# --- TEST VLSM BARU (SPESIFIKASI BAGIAN 6.3, 6.4, 6.5) ---
@pytest.mark.parametrize(
    "network_cidr,kebutuhan,expected_subnets",
    [
        (
            "192.168.1.0/24",
            [100, 50, 20, 2],
            [
                {"network_cidr": "192.168.1.0/25", "usable_hosts": 126},
                {"network_cidr": "192.168.1.128/26", "usable_hosts": 62},
                {"network_cidr": "192.168.1.192/27", "usable_hosts": 30},
                {"network_cidr": "192.168.1.224/30", "usable_hosts": 2},
            ]
        )
    ]
)
def test_alokasi_vlsm_success(network_cidr, kebutuhan, expected_subnets):
    from main import alokasi_vlsm
    hasil = alokasi_vlsm(network_cidr, kebutuhan)
    assert len(hasil) == len(expected_subnets)
    for res, exp in zip(hasil, expected_subnets):
        assert res["network_cidr"] == exp["network_cidr"]
        assert res["usable_hosts"] == exp["usable_hosts"]

@pytest.mark.parametrize(
    "network_cidr,kebutuhan",
    [
        ("192.168.1.0/24", [200, 100]), # Tidak muat
        ("192.168.1.1/24", [10, 5]),    # Network CIDR tidak valid (bukan network address)
        ("192.168.1.0/24", []),         # Kosong
    ]
)
def test_alokasi_vlsm_invalid(network_cidr, kebutuhan):
    from main import alokasi_vlsm
    with pytest.raises(ValueError):
        alokasi_vlsm(network_cidr, kebutuhan)

def test_api_vlsm_cases():
    # A07: Sukses 200
    response = client.post("/api/vlsm", json={"network": "192.168.1.0/24", "kebutuhan_host": [100, 50, 20, 2]})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    # A09: Input tidak valid mengembalikan 400 dengan field 'detail'
    response_err = client.post("/api/vlsm", json={"network": "192.168.1.0/24", "kebutuhan_host": [200, 100]})
    assert response_err.status_code == 400
    assert "detail" in response_err.json()

def test_alokasi_vlsm_kebutuhan_satu():
    # V05 di SPEC.md: kebutuhan 1 valid, blok minimal /30
    from main import alokasi_vlsm
    hasil = alokasi_vlsm("192.168.1.0/24", [1])
    assert hasil[0]["network_cidr"] == "192.168.1.0/30"