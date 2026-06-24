#!/usr/bin/env python3

import subprocess
import os
import sys


def banner():
    print("""
    ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
    ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
    ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
    ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
    ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
    ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
    Bug Bounty Recon Automation - by @HackSaf
    """)


def section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def create_output_dir(domain):
    base_dir = f"recon_{domain}"
    os.makedirs(base_dir, exist_ok=True)

    # count existing runs
    existing = [
        d for d in os.listdir(base_dir)
        if d.startswith("run_")
    ]

    run_number = len(existing) + 1
    output_dir = os.path.join(base_dir, f"run_{run_number}")

    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def run_subfinder(domain, output_dir):
    print(f"\n[*] Running Subfinder on {domain}...")
    output_file = f"{output_dir}/subdomains.txt"

    cmd = [
        "subfinder",
        "-d", domain,
        "-o", output_file,
        "-silent"
    ]

    subprocess.run(cmd)
    print(f"[+] Subdomains saved to {output_file}")
    return output_file


def run_httpx(input_file, output_file):
    print("\n[*] Probing for live hosts with httpx...")

    cmd = [
        "httpx",
        "-l", input_file,
        "-silent",
        "-o", output_file
    ]

    subprocess.run(cmd)
    print(f"[+] Live Hosts saved to {output_file}")
    return output_file


def run_alterx(subdomains_file, output_dir):
    print("\n[*] Generating Permutations with alterx...")

    output_file = f"{output_dir}/permutations.txt"

    with open(output_file, "w") as outfile:
        subprocess.run(
            ["alterx", "-l", subdomains_file],
            stdout=outfile
        )

    print(f"[+] Permutations saved to {output_file}")
    return output_file


def run_nuclei(live_hosts_file, output_dir):
    print("\n[*] Running Nuclei Vulnerability Scan...")

    output_file = f"{output_dir}/nuclei_results.txt"

    cmd = [
        "nuclei",
        "-l", live_hosts_file,
        "-severity", "critical,high,medium",
        "-silent",
        "-o", output_file
    ]

    subprocess.run(cmd)

    print(f"[+] Nuclei results saved to {output_file}")
    return output_file


def run_nmap(domain, output_dir):
    print(f"\n[*] Running Nmap port scan on {domain}...")

    output_file = f"{output_dir}/nmap_results.txt"

    cmd = [
        "nmap",
        "-sV",
        "--top-ports", "1000",
        domain,
        "-oN", output_file
    ]

    subprocess.run(cmd)

    print(f"[+] Nmap results saved to {output_file}")
    return output_file


def merge_files(file1, file2, output_file):
    seen = set()

    with open(output_file, "w") as out:
        for f in [file1, file2]:
            try:
                with open(f, "r") as inp:
                    for line in inp:
                        line = line.strip()

                        if not line:
                            continue

                        if line not in seen:
                            seen.add(line)
                            out.write(line + "\n")

            except FileNotFoundError:
                continue

    return output_file


def generate_report(domain, output_dir):
    print("\n[*] Generating CLEAN report...")

    report_file = f"{output_dir}/REPORT_{domain}.txt"

    def read_file(path):
        try:
            with open(path, "r") as f:
                return f.read().strip()
        except Exception:
            return "No data"

    subdomains = read_file(f"{output_dir}/subdomains.txt")
    live_hosts = read_file(f"{output_dir}/live_hosts.txt")
    permutations = read_file(f"{output_dir}/permutations.txt")
    perm_live_hosts = read_file(f"{output_dir}/perm_live_hosts.txt")
    nuclei = read_file(f"{output_dir}/nuclei_results.txt")
    nmap = read_file(f"{output_dir}/nmap_results.txt")

    with open(report_file, "w") as report:

        report.write("=====================================\n")
        report.write("        RECONNAISSANCE REPORT\n")
        report.write("=====================================\n\n")

        report.write(f"Target: {domain}\n")
        report.write(f"Date: {datetime.datetime.now()}\n")
        report.write("Tool: @HackSaf Recon Automation\n\n")

        report.write("=====================================\n")
        report.write("[ SUBDOMAINS ]\n")
        report.write("=====================================\n")
        report.write(subdomains + "\n\n")

        report.write("=====================================\n")
        report.write("[ LIVE HOSTS ]\n")
        report.write("=====================================\n")
        report.write(live_hosts + "\n\n")

        report.write("=====================================\n")
        report.write("[ PERMUTATIONS ]\n")
        report.write("=====================================\n")
        report.write(permutations + "\n\n")

        report.write("=====================================\n")
        report.write("[ PERMUTATION LIVE HOSTS ]\n")
        report.write("=====================================\n")
        report.write(perm_live_hosts + "\n\n")

        report.write("=====================================\n")
        report.write("[ NUCLEI FINDINGS ]\n")
        report.write("=====================================\n")
        report.write(nuclei + "\n\n")

        report.write("=====================================\n")
        report.write("[ NMAP RESULTS ]\n")
        report.write("=====================================\n")
        report.write(nmap + "\n\n")

    print(f"\n[✓] CLEAN Report Generated: {report_file}")


def main():
    banner()

    if len(sys.argv) != 2:
        print("Usage: recon <target-domain>")
        print("Example: recon example.com")
        sys.exit(1)

    domain = sys.argv[1]

    output_dir = create_output_dir(domain)

    print(f"[+] Target: {domain}")
    print(f"[+] Output Directory: {output_dir}")

    section("STAGE 1 — Subdomain Enumeration")

    subdomains_file = run_subfinder(domain, output_dir)

    live_hosts_file = run_httpx(
        subdomains_file,
        f"{output_dir}/live_hosts.txt"
    )

    permutations_file = run_alterx(
        subdomains_file,
        output_dir
    )

    perm_live_hosts = run_httpx(
        permutations_file,
        f"{output_dir}/perm_live_hosts.txt"
    )

    all_live_hosts = merge_files(
        live_hosts_file,
        perm_live_hosts,
        f"{output_dir}/all_live_hosts.txt"
    )

    section("STAGE 2 — Vulnerability Scan")
    run_nuclei(all_live_hosts, output_dir)

    section("STAGE 3 — Port Scan")
    run_nmap(domain, output_dir)

    section("STAGE 4 — Report Generation")
    generate_report(domain, output_dir)


if __name__ == "__main__":
    main()
