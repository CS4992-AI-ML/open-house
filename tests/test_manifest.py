from chalice_app.chalicelib.manifest_json import get_manifest_json


def test_get_manifest():
    return get_manifest_json()


output = test_get_manifest()
print(output)
