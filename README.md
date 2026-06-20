# Azure-Foundry

Welcome to Azure-Foundry — a hands-on learning repository for exploring Azure Foundry concepts, automation, and lab exercises using Python and shell scripting.

> Learning Azure Foundry

Table of Contents

- Project overview
- What I learned (key takeaways)
- Learning goals
- Repository structure
- Lab environment & prerequisites
- How to run the labs (step-by-step)
- Example: running a Python lab script
- Recommended workflow
- Notes about security and costs
- Troubleshooting
- Contributing
- License & contact

Project overview

This repository contains guided lab files, example scripts, and notes intended to help learners experiment with components and workflows related to "Azure Foundry" topics. The content is primarily practical, focusing on automation with the Azure CLI and Python scripts to deploy, validate, and tear down sample resources.

What I learned (key takeaways)

Below are specific concepts and practical skills I gained while working through the labs in this repository:

- Azure account and subscription management
  - How to authenticate with the Azure CLI (`az login`) and target a specific subscription using `az account set --subscription <SUB_ID>`.
  - How different subscriptions and roles affect provisioning and billing.

- Resource lifecycle and cost awareness
  - How to design labs to create resources reproducibly and tear them down to avoid lingering costs.
  - The importance of checking SKU and region availability before provisioning.

- Automation using Python and the Azure SDK / CLI
  - Structure of idempotent scripts: separate deploy and cleanup steps, check for existing resources before creating, and use meaningful logging and exit codes.
  - Using the Azure CLI programmatically (subprocess calls) and the azure management SDKs when finer control is needed.
  - Using `requirements.txt` and virtual environments to keep dependencies isolated.

- Service principals, authentication patterns, and least privilege
  - Creating service principals for automation and assigning minimal required RBAC roles.
  - How managed identities can be a safer alternative for automation running inside Azure.

- Networking and resource configuration best practices
  - Understanding virtual networks, subnets, NSGs, and their role in isolating lab resources.
  - Basic patterns for securely exposing resources for verification (temporary public IPs, SSH jump hosts, port forwarding) and cleaning them up afterwards.

- Shell tooling and JSON processing
  - Use of `jq` for parsing CLI JSON output in shell scripts to extract resource IDs and statuses.
  - Writing robust shell scripts with error checks and useful user prompts.

- Testing, verification, and idempotent cleanup
  - Adding verification steps (CLI checks or small test scripts) after deployment to confirm resources are configured as intended.
  - Implementing `cleanup_lab.py` or `cleanup.sh` to remove created resources safely.

- Documentation and reproducibility
  - The value of clear per-lab README files with expected run time, required SKUs, and approximate cost estimates.
  - Documenting environment variables and configuration file formats so others can reproduce the setup.

Learning goals

- Understand core Azure Foundry concepts and typical workflows.
- Automate provisioning and management tasks using Python and the Azure CLI.
- Run step-by-step labs to deploy sample resources, validate configuration, and tear down environments safely.
- Capture reproducible examples that can be extended into automation pipelines.

Repository structure

At a glance:

- Labfiles/ — Primary folder containing lab exercises, example scripts, and supporting assets.
  - Each lab is usually self-contained in a subfolder (e.g., Lab1/, Lab2/) and contains README or instructions specific to that lab.
- requirements.txt — If present, lists Python dependencies used across labs.
- scripts/ or tools/ — Helper scripts for common tasks.

Note: The repository language composition is mostly Python with a small portion of shell scripts.

Lab environment & prerequisites

Before running the labs you will typically need:

- An Azure subscription with sufficient permissions to create and delete resources.
- Azure CLI (az) installed and signed in: https://learn.microsoft.com/cli/azure/install-azure-cli
- Python 3.8+ and pip
- (Recommended) virtualenv or venv to isolate dependencies
- jq (optional) for JSON processing in shell-based examples

How to run the labs (step-by-step)

1. Clone the repository and inspect the Labfiles folder.

```bash
git clone https://github.com/aman-jnu/Azure-Foundry.git
cd Azure-Foundry/Labfiles
ls -la
```

2. Create and activate a Python virtual environment (recommended).

```bash
# macOS / Linux
python -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install Python dependencies if a `requirements.txt` exists at repo root or per-lab.

```bash
pip install -r ../requirements.txt   # or inside each lab folder if present
```

4. Authenticate with Azure and set your subscription.

```bash
az login
az account set --subscription "<SUBSCRIPTION_ID_OR_NAME>"
```

If you prefer non-interactive automation, create a service principal and export credentials as environment variables (only for automation runs, not interactive learning):

```bash
# Create a service principal (example)
az ad sp create-for-rbac --name "azfoundry-lab-sp" --role "Contributor" --scopes "/subscriptions/<SUBSCRIPTION_ID>"
# The command prints appId, password, and tenant - export those when used by automation scripts.
export AZURE_CLIENT_ID="<appId>"
export AZURE_CLIENT_SECRET="<password>"
export AZURE_TENANT_ID="<tenant>"
```

5. Pick a lab directory and read its README.

```bash
cd Labfiles/Lab1
less README.md
```

6. Update any lab-specific configuration files or environment variables. Typical variables:

- RESOURCE_PREFIX or PROJECT_NAME
- LOCATION or AZURE_REGION
- ADMIN_USERNAME / SSH_PUBLIC_KEY
- SUBSCRIPTION_ID

7. Run the deploy script for the lab (example names used; check each lab's README):

```bash
# Python example
python deploy_lab.py

# Shell example
./deploy_lab.sh
```

8. Verify results as described in the lab README. Typical verification steps:

- `az resource list` or `az vm show` to check resource status
- curl / SSH into deployed endpoints if applicable
- Run provided verification scripts: `python verify_lab.py`

9. Tear down resources when done to avoid costs:

```bash
python cleanup_lab.py
# or
./cleanup_lab.sh
```

Example: running a Python lab script

```bash
cd Labfiles/Lab1
# ensure virtual environment is active
python deploy_lab.py --prefix mylab --location eastus
# wait for provisioning to complete or follow the script output
python verify_lab.py --resource-group mylab-rg
python cleanup_lab.py --resource-group mylab-rg
```

Recommended workflow

- Work in a feature branch for any updates you make to labs or scripts.
- Keep configuration values (secrets, credentials) out of the repo. Use environment variables or Azure Key Vault.
- Add clear README instructions in any new lab folder you add, including expected time to run and approximate cost.

Notes about security and costs

- Labs will often create billable Azure resources. Always review resource types and estimated costs before provisioning.
- Never commit credentials, secrets, or service principal keys to the repository. Use environment variables, Azure Key Vault, or managed identities.
- Limit permissions of any service principals used for automation and follow the principle of least privilege.

Troubleshooting

- az login fails / interactive auth not wanted: create a service principal for automation.
- Permission denied / 403: verify your account's role assignments and that the subscription is correct.
- Resource quota or SKU not available: try a different region or smaller SKU, and clean up failed partial deployments.
- Long-running resources: many resources take time to provision — add polling or checks in scripts and use `--no-wait` consciously.

Contributing

Contributions are welcome. Suggested ways to contribute:

- Open an issue describing a bug, improvement, or new lab idea.
- Fork and create a pull request with fixes or new lab content.
- Add clear step-by-step instructions and notes about required Azure SKU sizes and permissions.

When submitting changes, please include:

- A short description of the change
- How to reproduce or run the lab
- Any new prerequisites or costs

License

This repository does not include a LICENSE file by default. If you want others to reuse the content under a specific license, add a LICENSE (for example, MIT) to the repository.

Contact

For questions related to these labs, open an issue in the repository or contact the repository owner.

---

Next steps I can take for you:

- Scan Labfiles/ and insert a per-lab index into this README with short summaries (I can do this now).
- Create or update lab-specific README files inside Labfiles/ with step-by-step commands tailored to each exercise.
- Add a requirements.txt if Python dependencies are present.

Tell me which you'd like and I'll proceed.
