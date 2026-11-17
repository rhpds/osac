import copy
import importlib.util
from pathlib import Path
import unittest

path = Path(__file__).parents[1] / "runtime-automation/scripts/validate-caas.py"
spec = importlib.util.spec_from_file_location("caas", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CaasTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = {
            "order": {"metadata": {"name": "order-fixture"}, "status": {"phase": "Ready"}},
            "bmh": {"metadata": {"name": "virtual-bmh-1", "namespace": "osac"},
                    "spec": {"online": True, "consumerRef": {"name": "bmi-fixture", "namespace": "osac", "uid": "fixture-uid"}},
                    "status": {"provisioning": {"state": "provisioned"}, "hardware": {"nics": [{"ip": "192.0.2.10"}]}}},
            "bmi": {"metadata": {"name": "bmi-fixture", "uid": "fixture-uid"}, "status": {"phase": "Ready"}},
            "hc": {"metadata": {"name": "order-fixture", "namespace": "osac-order-fixture"},
                   "status": {"conditions": [{"type": "Available", "status": "True"}]}},
            "nodepools": [{"spec": {"clusterName": "order-fixture", "replicas": 1},
                           "status": {"readyReplicas": 1}}],
            "nodes": [{"metadata": {"name": "worker-1", "labels": {"node-role.kubernetes.io/worker": ""}},
                       "status": {"conditions": [{"type": "Ready", "status": "True"}],
                                  "addresses": [{"type": "InternalIP", "address": "192.0.2.10"}]}}],
        }

    def test_current_topology_passes(self):
        module.validate_snapshot(self.snapshot)

    def test_unready_order_or_unprovisioned_host_fails(self):
        for key, field, value in [("order", "phase", "Progressing"), ("bmi", "phase", "Failed")]:
            snapshot = copy.deepcopy(self.snapshot)
            snapshot[key]["status"][field] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                module.validate_snapshot(snapshot)
        self.snapshot["bmh"]["status"]["provisioning"]["state"] = "available"
        with self.assertRaises(ValueError):
            module.validate_snapshot(self.snapshot)

    def test_unrelated_ready_worker_does_not_satisfy_lab(self):
        self.snapshot["nodes"][0]["status"]["addresses"][0]["address"] = "192.0.2.99"
        with self.assertRaises(ValueError):
            module.validate_snapshot(self.snapshot)

    def test_wrong_consumer_or_hosted_cluster_fails(self):
        for resource, field, value in [("bmi", "uid", "different-instance"),
                                        ("hc", "namespace", "another-order-namespace")]:
            snapshot = copy.deepcopy(self.snapshot)
            snapshot[resource]["metadata"][field] = value
            with self.subTest(resource=resource), self.assertRaises(ValueError):
                module.validate_snapshot(snapshot)

    def test_unready_nodepool_or_hosted_cluster_fails(self):
        snapshot = copy.deepcopy(self.snapshot)
        snapshot["nodepools"][0]["status"]["readyReplicas"] = 0
        with self.assertRaises(ValueError):
            module.validate_snapshot(snapshot)
        self.snapshot["hc"]["status"]["conditions"][0]["status"] = "False"
        with self.assertRaises(ValueError):
            module.validate_snapshot(self.snapshot)


if __name__ == "__main__":
    unittest.main()
