# Virtualization and Cloud Computing — Comprehensive Guide

## CIS 411 | Portland Community College | Spring 2026

| Field             | Value                              |
|-------------------|------------------------------------|
| **Author**        | Preston Furulie                    |
| **Organization**  | FLLC Enterprise                    |
| **Department**    | Platform Engineering               |
| **Alignment**     | CompTIA Cloud+ (CV0-003)           |

---

## 1. Hypervisor Types

A **hypervisor** (Virtual Machine Monitor) is software that creates and manages
virtual machines by abstracting the underlying physical hardware.

### 1.1 Type 1 — Bare-Metal Hypervisors

Type 1 hypervisors run directly on server hardware without a host operating system.
They provide near-native performance and are the standard for enterprise datacenters.

| Hypervisor            | Vendor      | License         | Key Features                        |
|-----------------------|-------------|-----------------|-------------------------------------|
| VMware ESXi           | Broadcom    | Commercial      | vMotion, HA, DRS, vSAN             |
| Microsoft Hyper-V     | Microsoft   | Included w/ Server | Live Migration, Replica, S2D    |
| KVM                   | Open Source | Free (GPL)      | Linux-native, libvirt, QEMU        |
| Citrix Hypervisor     | Cloud.com   | Commercial/Free | XenMotion, GPU passthrough         |
| Oracle VM Server      | Oracle      | Free            | Oracle workload optimized           |

**Advantages of Type 1:**
- Direct hardware access for maximum performance
- Lower overhead (no host OS consuming resources)
- Enterprise management tools (vCenter, SCVMM)
- Hardware-level isolation between VMs

### 1.2 Type 2 — Hosted Hypervisors

Type 2 hypervisors run as applications on top of a standard operating system.
They are used for development, testing, and desktop virtualization.

| Hypervisor                | Vendor      | Host OS              | Best For                     |
|---------------------------|-------------|----------------------|------------------------------|
| Oracle VirtualBox         | Oracle      | Windows/macOS/Linux  | Lab environments, learning   |
| VMware Workstation Pro    | Broadcom    | Windows/Linux        | Professional development     |
| VMware Fusion             | Broadcom    | macOS                | Mac-based development        |
| Parallels Desktop         | Parallels   | macOS                | Running Windows on Mac       |
| GNOME Boxes               | GNOME       | Linux                | Simple Linux VM management   |

**Advantages of Type 2:**
- Easy installation on existing workstations
- No dedicated server hardware required
- Snapshot and clone capabilities for testing
- Lower barrier to entry for learning virtualization

### 1.3 Type 1 vs Type 2 Comparison

| Feature             | Type 1 (Bare-Metal)           | Type 2 (Hosted)               |
|---------------------|-------------------------------|-------------------------------|
| Performance         | Near-native                   | Some overhead from host OS    |
| Use Case            | Production workloads          | Development / testing         |
| Hardware Access     | Direct                        | Through host OS               |
| Management          | Enterprise consoles           | Desktop application           |
| Cost                | Higher (dedicated hardware)   | Lower (runs on workstation)   |
| Scalability         | Hundreds of VMs               | Handful of VMs                |

---

## 2. Virtual Machine Components

### 2.1 VM Resource Allocation

| Component        | Physical Equivalent | Configuration Options                    |
|------------------|--------------------|-----------------------------------------|
| **vCPU**         | CPU cores          | Number of sockets and cores per socket  |
| **vRAM**         | Physical RAM       | Allocated in MB/GB, can overcommit      |
| **vNIC**         | Network adapter    | Virtual switch, VLAN tagging, teaming   |
| **Virtual Disk** | Hard drive         | Thin/thick provisioned, VMDK/VHD/QCOW2 |
| **vGPU**         | Graphics card      | Passthrough or shared GPU profiles      |
| **CD/DVD**       | Optical drive      | ISO image mount                         |

### 2.2 Virtual Disk Types

| Provisioning   | Description                                    | Pros / Cons                      |
|----------------|------------------------------------------------|----------------------------------|
| Thin           | Grows as data is written                       | Saves space / risk of overcommit |
| Thick Eager    | Full space allocated and zeroed at creation     | Best performance / wastes space  |
| Thick Lazy     | Full space allocated, zeroed on first write     | Balance of space and performance |

### 2.3 Virtual Networking

| Network Type     | Description                                        |
|------------------|----------------------------------------------------|
| Virtual Switch   | Software-defined switch connecting VMs              |
| Port Group       | VLAN assignment and policy group on a vSwitch       |
| Distributed Switch| Centrally managed switch spanning multiple hosts   |
| NAT              | VMs share host IP for outbound traffic             |
| Bridged          | VMs appear as physical devices on the network      |
| Host-Only        | VMs communicate only with host and each other      |

---

## 3. Cloud Service Models

### 3.1 The Cloud Computing Stack

```
┌─────────────────────────────────────────┐
│           SaaS                          │  ← You manage: Nothing (just use it)
│  Gmail, Microsoft 365, Salesforce       │
├─────────────────────────────────────────┤
│           PaaS                          │  ← You manage: Applications + Data
│  Azure App Service, Heroku, Google App  │
├─────────────────────────────────────────┤
│           IaaS                          │  ← You manage: OS + Applications + Data
│  AWS EC2, Azure VMs, Google Compute     │
├─────────────────────────────────────────┤
│     On-Premises                         │  ← You manage: Everything
│  Your datacenter, your hardware         │
└─────────────────────────────────────────┘
```

### 3.2 Service Model Comparison

| Model  | You Manage                    | Provider Manages                        | Examples                         |
|--------|-------------------------------|-----------------------------------------|----------------------------------|
| IaaS   | OS, middleware, apps, data    | Hardware, networking, virtualization    | AWS EC2, Azure VMs, GCP Compute  |
| PaaS   | Applications, data           | OS, middleware, runtime, hardware       | Heroku, Azure App Service, GAE   |
| SaaS   | Data (your content)          | Everything else                         | Microsoft 365, Gmail, Salesforce |

### 3.3 Additional Service Models

| Model  | Description                                      | Examples                          |
|--------|--------------------------------------------------|-----------------------------------|
| FaaS   | Function as a Service (serverless compute)       | AWS Lambda, Azure Functions       |
| DaaS   | Desktop as a Service                             | Azure Virtual Desktop, Amazon WorkSpaces |
| DBaaS  | Database as a Service                            | AWS RDS, Azure SQL, Cloud SQL     |
| CaaS   | Container as a Service                           | AWS ECS, Azure Container Instances|
| STaaS  | Storage as a Service                             | AWS S3, Azure Blob, Google Cloud Storage |

---

## 4. Cloud Deployment Models

### 4.1 Deployment Model Comparison

| Model         | Description                                   | Best For                           |
|---------------|-----------------------------------------------|------------------------------------|
| Public Cloud  | Resources shared across tenants on provider infra | Startups, variable workloads    |
| Private Cloud | Dedicated infrastructure for a single org     | Regulated industries, compliance   |
| Hybrid Cloud  | Mix of on-premises and public cloud           | Gradual migration, data residency  |
| Multi-Cloud   | Using services from multiple cloud providers  | Avoid vendor lock-in, best-of-breed|
| Community Cloud| Shared among organizations with common needs | Government, healthcare consortiums |

### 4.2 Cloud Migration Strategies (The 6 R's)

| Strategy      | Description                                    | When to Use                        |
|---------------|------------------------------------------------|------------------------------------|
| Rehost        | Lift and shift — move as-is                    | Quick migration, minimal changes   |
| Replatform    | Lift and reshape — minor optimizations         | Some cloud benefits without rewrite|
| Repurchase    | Replace with SaaS equivalent                   | Commodity workloads (email, CRM)   |
| Refactor      | Re-architect for cloud-native                  | Maximum cloud benefits needed      |
| Retain        | Keep on-premises                               | Not a good candidate for cloud     |
| Retire        | Decommission the application                   | No longer needed                   |

---

## 5. AWS / Azure / GCP Service Comparison

| Service Category     | AWS                        | Azure                       | GCP                          |
|----------------------|----------------------------|-----------------------------|------------------------------|
| Compute (VMs)        | EC2                        | Virtual Machines            | Compute Engine               |
| Serverless           | Lambda                     | Functions                   | Cloud Functions              |
| Container Orchestration | EKS                     | AKS                        | GKE                          |
| Object Storage       | S3                         | Blob Storage                | Cloud Storage                |
| Block Storage        | EBS                        | Managed Disks               | Persistent Disk              |
| Relational DB        | RDS                        | Azure SQL                   | Cloud SQL                    |
| NoSQL DB             | DynamoDB                   | Cosmos DB                   | Firestore / Bigtable         |
| Virtual Network      | VPC                        | VNet                        | VPC                          |
| DNS                  | Route 53                   | Azure DNS                   | Cloud DNS                    |
| Load Balancer        | ELB/ALB/NLB               | Azure Load Balancer         | Cloud Load Balancing         |
| CDN                  | CloudFront                 | Azure CDN / Front Door      | Cloud CDN                    |
| Identity (IAM)       | IAM                        | Entra ID (Azure AD)         | Cloud IAM                    |
| Monitoring           | CloudWatch                 | Azure Monitor               | Cloud Monitoring             |
| AI/ML Platform       | SageMaker                  | Azure AI                    | Vertex AI                    |
| CI/CD                | CodePipeline               | Azure DevOps                | Cloud Build                  |

---

## 6. Containers vs Virtual Machines

### 6.1 Architecture Comparison

```
Virtual Machines:                    Containers:
┌──────┐ ┌──────┐ ┌──────┐         ┌──────┐ ┌──────┐ ┌──────┐
│ App A│ │ App B│ │ App C│         │ App A│ │ App B│ │ App C│
├──────┤ ├──────┤ ├──────┤         ├──────┤ ├──────┤ ├──────┤
│ Bins │ │ Bins │ │ Bins │         │ Bins │ │ Bins │ │ Bins │
├──────┤ ├──────┤ ├──────┤         └──────┘ └──────┘ └──────┘
│Guest │ │Guest │ │Guest │         ┌────────────────────────────┐
│  OS  │ │  OS  │ │  OS  │         │    Container Runtime       │
├──────┴─┴──────┴─┴──────┤         ├────────────────────────────┤
│       Hypervisor        │         │       Host OS              │
├─────────────────────────┤         ├────────────────────────────┤
│       Hardware          │         │       Hardware             │
└─────────────────────────┘         └────────────────────────────┘
```

### 6.2 Feature Comparison

| Feature           | Virtual Machines              | Containers                      |
|-------------------|-------------------------------|---------------------------------|
| Isolation         | Full OS-level (stronger)      | Process-level (lighter)         |
| Boot Time         | Minutes                       | Seconds                         |
| Size              | GBs (includes full OS)        | MBs (shares host kernel)        |
| Density           | Tens per host                 | Hundreds per host               |
| Portability       | Hypervisor-dependent          | Runs anywhere with runtime      |
| Use Case          | Legacy apps, full OS needs    | Microservices, CI/CD            |
| Overhead          | Higher (full OS per VM)       | Minimal (shared kernel)         |

### 6.3 Docker Overview

**Key Docker Concepts:**

| Concept         | Description                                          |
|-----------------|------------------------------------------------------|
| Image           | Read-only template containing application and deps   |
| Container       | Running instance of an image                         |
| Dockerfile      | Text file with instructions to build an image        |
| Registry        | Repository for storing and distributing images       |
| Volume          | Persistent storage that survives container lifecycle  |
| Network         | Virtual network connecting containers                |
| Docker Compose  | Tool for defining multi-container applications       |

### 6.4 Kubernetes Overview

Kubernetes (K8s) is the industry-standard container orchestration platform.

| Component        | Description                                         |
|------------------|-----------------------------------------------------|
| Pod              | Smallest deployable unit (one or more containers)   |
| Node             | Worker machine running pods                         |
| Cluster          | Set of nodes managed by a control plane             |
| Service          | Stable network endpoint for accessing pods          |
| Deployment       | Declarative definition of desired pod state         |
| Namespace        | Virtual cluster for resource isolation              |
| ConfigMap/Secret | Configuration and sensitive data management         |
| Ingress          | External HTTP/HTTPS routing to services             |

---

## 7. Serverless Computing

### 7.1 Serverless Characteristics

| Characteristic       | Description                                       |
|----------------------|---------------------------------------------------|
| No server management | Provider handles all infrastructure               |
| Auto-scaling         | Scales from zero to thousands automatically       |
| Pay-per-execution    | Billed only when code runs (per request + duration)|
| Event-driven         | Triggered by events (HTTP, queue, schedule, etc.) |
| Stateless            | Functions don't maintain state between invocations|
| Short-lived          | Execution time limits (typically 5-15 minutes)    |

### 7.2 Serverless Use Cases

| Use Case                 | Example                                        |
|--------------------------|------------------------------------------------|
| API backends             | REST API handling with Lambda + API Gateway    |
| File processing          | Thumbnail generation on S3 upload              |
| Scheduled tasks          | Nightly database cleanup, report generation    |
| Real-time data           | Stream processing from IoT devices             |
| Chatbots                 | Natural language processing triggers           |
| Authentication           | Custom auth logic for API access               |

### 7.3 Serverless Limitations

- **Cold starts**: Initial invocation latency when function hasn't run recently
- **Execution limits**: Maximum runtime, memory, and payload size constraints
- **Vendor lock-in**: Functions tied to specific provider's event model
- **Debugging complexity**: Distributed tracing harder than monolithic apps
- **Cost unpredictability**: Very high traffic can become expensive

---

## 8. Cloud Security — Shared Responsibility Model

### 8.1 Responsibility Matrix

| Security Layer          | IaaS              | PaaS              | SaaS              |
|-------------------------|--------------------|--------------------|--------------------|
| Data classification     | Customer           | Customer           | Customer           |
| Client/endpoint security| Customer           | Customer           | Customer           |
| Identity & access mgmt  | Customer           | Customer           | Shared             |
| Application security    | Customer           | Customer           | Provider           |
| Network controls        | Customer           | Shared             | Provider           |
| Operating system        | Customer           | Provider           | Provider           |
| Physical hosts          | Provider           | Provider           | Provider           |
| Physical network        | Provider           | Provider           | Provider           |
| Physical datacenter     | Provider           | Provider           | Provider           |

### 8.2 Cloud Security Best Practices

| Practice                    | Description                                     |
|-----------------------------|-------------------------------------------------|
| Least privilege             | Grant minimum permissions needed for each role  |
| MFA everywhere              | Require multi-factor on all cloud console access|
| Encryption at rest          | Enable default encryption for storage services  |
| Encryption in transit       | Use TLS/HTTPS for all data transmission         |
| Network segmentation        | Use VPCs, subnets, security groups, NACLs       |
| Logging and monitoring      | Enable CloudTrail/Azure Monitor/GCP Audit Logs  |
| Patch management            | Keep OS and applications updated (IaaS)         |
| Backup and DR               | Implement cross-region replication              |
| Compliance frameworks       | Align with SOC 2, ISO 27001, HIPAA as needed    |
| Regular security assessments| Penetration testing and vulnerability scanning  |

### 8.3 Identity and Access Management (IAM)

| Concept             | Description                                         |
|---------------------|-----------------------------------------------------|
| User                | Individual identity with credentials                |
| Group               | Collection of users for bulk permission management  |
| Role                | Assumable identity with temporary credentials       |
| Policy              | JSON/YAML document defining allowed/denied actions  |
| Service Account     | Non-human identity for application access           |
| Federation          | Trust external identity providers (SAML, OIDC)      |

---

## References

- CompTIA Cloud+ CV0-003 Exam Objectives
- AWS Well-Architected Framework
- Microsoft Azure Architecture Center
- Google Cloud Architecture Framework
- Docker Documentation
- Kubernetes Documentation

---

*FLLC Enterprise — Platform Engineering Division*
*Author: Preston Furulie | Portland Community College | Spring 2026*
