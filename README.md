# Azure-Foundry

Welcome to Azure-Foundry — a hands-on learning repository for exploring Azure Foundry concepts, automation, and lab exercises using Python and shell scripting.

> Learning Azure Foundry

Table of Contents

- Project overview
- Learning goals
- Repository structure
- Lab environment & prerequisites
- How to run the labs
- Recommended workflow
- Notes about security and costs
- Contributing
- License & contact

Project overview

This repository contains guided lab files, example scripts, and notes intended to help learners experiment with components and workflows related to "Azure Foundry" topics. The content is primarily implemented in Python with some shell scripts for automation and environment setup.

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

Example commands to prepare your environment:

```bash
# Login to Azure
az login

# Set target subscription (replace SUB_ID)
az account set --subscription SUB_ID

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows (PowerShell: .\.venv\Scripts\Activate.ps1)

# Install Python dependencies if requirements.txt exists
pip install -r requirements.txt
```

How to run the labs

1. Open the Labfiles/ folder and read the lab-specific README or instructions for each exercise.
2. Follow the lab steps in order. Typical steps include:
   - Inspect the lab README for objectives and architecture diagrams.
   - Review any configuration files (variables, parameter files) and update them with your subscription/resource names.
   - Run provided Python scripts or shell scripts to provision resources.
   - Validate deployments using Azure CLI or portal and then run verification scripts.
   - Tear down resources to avoid unexpected costs using provided cleanup scripts.

Example: running a Python lab script

```bash
cd Labfiles/Lab1
# if the lab uses a virtual environment, make sure it's activated
python deploy_lab.py
# verify status, then cleanup
python cleanup_lab.py
```

Repository contents (auto-generated overview)

Below is a short, generated listing of the top-level Labfiles directory and its immediate subfolders. This is meant to help you quickly find lab exercises and should be updated periodically.

- Labfiles/
  - (each lab folder contains its own README and scripts)

If you want, I can scan the Labfiles/ directory and auto-generate a detailed per-lab index here.

Recommended workflow

- Work in a feature branch for any updates you make to labs or scripts.
- Keep configuration values (secrets, credentials) out of the repo. Use environment variables or Azure Key Vault.
- Add clear README instructions in any new lab folder you add, including expected time to run and approximate cost.

Notes about security and costs

- Labs will often create billable Azure resources. Always review resource types and estimated costs before provisioning.
- Never commit credentials, secrets, or service principal keys to the repository. Use environment variables, Azure Key Vault, or managed identities.
- Limit permissions of any service principals used for automation and follow the principle of least privilege.

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