import logging
import secrets

from typing import List

from podman_decompose.util import run

log = logging.getLogger(__name__)


def decompose(obj: dict) -> None:
    networks = decompose_networks(obj)
    for network in networks.values():
        run(network["command"])
    ordered_services = get_ordered_services(obj)
    for svc_name in ordered_services:
        svc = obj["services"][svc_name]
        replicas = svc.get("deploy", dict()).get("replicas", 1)
        if replicas == 0:
            log.warning(f"replicas for service {svc_name} is set to 0; skipping")
            continue
        if replicas > 1:
            for i in range(replicas):
                svc_name_ = f"{svc_name}_{i}"
                run(decompose_service(svc_name, svc, networks, indexed_name=svc_name_))
            continue
        run(decompose_service(svc_name, svc, networks))


def destroy(obj: dict) -> None:
    ordered_services = get_ordered_services(obj)
    if ordered_services:
        run(["podman", "container", "rm", "-f"] + ordered_services)
    networks = decompose_networks(obj)
    if networks:
        run(["podman", "network", "rm", "-f"] + list(networks.keys()))


def decompose_networks(obj) -> dict:
    networks_set = set()
    for name, svc in obj["services"].items():
        if "links" in svc:
            networks_set.add((name,) + tuple(svc["links"]))
    networks = dict()
    for services in networks_set:
        net_name = secrets.token_hex(4)
        networks[net_name] = dict(
            command=["podman", "network", "create", net_name],
            services=services,
        )
    return networks


def get_ordered_services(obj: dict) -> List[str]:
    services = list(obj["services"].keys())
    for name, svc in obj["services"].items():
        deps = svc.get("depends_on", list())
        if isinstance(deps, dict):
            deps = list(deps.keys())
        if deps:
            for dep in deps:
                svc_index = services.index(name)
                dep_index = services.index(dep)
                if svc_index < dep_index:
                    services.pop(dep_index)
                    services.insert(svc_index, dep)
    return services


def decompose_service(
    name: str, obj: dict, networks: dict, indexed_name: str = ""
) -> List[str]:
    cmd = ["podman", "run", "--rm", "-i", "-d"]
    environment = obj.get("environment")
    if isinstance(environment, list):
        for item in environment:
            cmd.extend(["-e", item])
    elif isinstance(environment, dict):
        for k, v in environment.items():
            v = v or ""
            cmd.extend(["-e", f"{k}={v}"])
    for item in obj.get("volumes", []):
        cmd.extend(["-v", item])
    for item in obj.get("ports", []):
        cmd.extend(["-p", item])
    healthcheck = obj.get("healthcheck")
    if healthcheck:
        health_cmd = healthcheck["test"]
        if isinstance(health_cmd, list):
            health_cmd = " ".join(health_cmd)
        if "test" in healthcheck:
            cmd.extend(["--health-cmd", health_cmd])
        if "start_period" in healthcheck:
            cmd.extend(["--health-start-period", healthcheck["start_period"]])
        if "interval" in healthcheck:
            cmd.extend(["--health-interval", healthcheck["interval"]])
        if "retries" in healthcheck:
            cmd.extend(["--health-retries", healthcheck["retries"]])
        if "timeout" in healthcheck:
            cmd.extend(["--health-timeout", healthcheck["timeout"]])
    if networks:
        for net_name, network in networks.items():
            if name in network["services"]:
                cmd.extend(["--network", net_name])
    cmd.extend(["--name", indexed_name or name])
    if "image" in obj:
        cmd.append(obj["image"])
    return cmd
