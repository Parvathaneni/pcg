# Proposed Repository Structure

```text
ABC-fast-Implementation/
├── fast/
│   └── stages/
│       ├── 0-org-setup/
│       └── 2-project-factory/
│
├── modules/
│   ├── bigquery-dataset/
│   ├── billing-account/
│   ├── folder/
│   ├── gcs/
│   ├── iam-service-account/
│   ├── kms/
│   ├── logging-bucket/
│   ├── organization/
│   ├── project-factory/
│   ├── project/
│   └── pubsub/
│
├── orgs/
│   ├── sandbox/
│   │   ├── stage-0.tfvars
│   │   ├── stage-2.tfvars
│   │   ├── defaults.yaml
│   │   ├── folders/
│   │   ├── iam/
│   │   ├── org-policies/
│   │   ├── billing-accounts/
│   │   ├── project-factory/
│   │   │   └── testing-projects/
│   │   │       ├── test-app-001.yaml
│   │   │       └── test-shared-vpc.yaml
│   │   └── sandbox-only/
│   │       └── experimental-org-iam.tfvars
│   │
│   └── prod/
│       ├── stage-0.tfvars
│       ├── stage-2.tfvars
│       ├── defaults.yaml
│       ├── folders/
│       ├── iam/
│       ├── org-policies/
│       ├── billing-accounts/
│       └── project-factory/
│           ├── app-projects/
│           │   ├── claims-prod.yaml
│           │   └── billing-prod.yaml
│           ├── shared-services/
│           ├── networking/
│           └── security/
│
├── backends/
│   ├── sandbox/
│   │   ├── stage-0.hcl
│   │   └── stage-2.hcl
│   └── prod/
│       ├── stage-0.hcl
│       └── stage-2.hcl
│
├── harness/
│   ├── sandbox/
│   │   ├── gcp-sandbox-stage0.md
│   │   └── gcp-sandbox-stage2.md
│   └── prod/
│       ├── gcp-prod-stage0.md
│       └── gcp-prod-stage2.md
│
├── docs/
│   ├── branching-model.md
│   ├── promotion-flow.md
│   └── project-onboarding.md
│
├── .github/
│   └── CODEOWNERS
│
├── .gitignore
├── README.md
├── default-versions.tf
└── imports.txt
```
