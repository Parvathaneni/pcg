abc-fast-Implementation/
├── fast/
│   └── stages/
│       ├── 0-org-setup/
│       ├── 1-resource-management/
│       └── 2-project-factory/
│
├── modules/
│   └── enterprise/
│
├── orgs/
│   ├── sandbox/
│   │   ├── stage-0.tfvars
│   │   ├── stage-1.tfvars
│   │   ├── stage-2.tfvars
│   │   ├── folders.yaml
│   │   ├── iam.yaml
│   │   ├── org-policies.yaml
│   │   ├── networking.yaml
│   │   └── project-factory/
│   │       └── testing-projects/
│   │           ├── test-app-001.yaml
│   │           └── test-shared-vpc.yaml
│   │
│   └── prod/
│       ├── stage-0.tfvars
│       ├── stage-1.tfvars
│       ├── stage-2.tfvars
│       ├── folders.yaml
│       ├── iam.yaml
│       ├── org-policies.yaml
│       ├── networking.yaml
│       └── project-factory/
│           ├── app-projects/
│           │   ├── claims-prod.yaml
│           │   └── billing-prod.yaml
│           ├── shared-services/
│           ├── networking/
│           └── security/
│
│
│
└── .github/
    └── CODEOWNERS
