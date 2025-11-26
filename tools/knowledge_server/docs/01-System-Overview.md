---
**Auto-Generated Documentation**  
Generated: 2025-11-25T15:41:11.325404  
Branch: master  
Path: Trunk/FrontierOM  
**⚠️ Do not edit directly - regenerate from code**
---


# System Overview


    **EOC Order Care - Cordys/OpenText BPM System**

    **Architecture:**
    - Platform: Cordys/OpenText BPM
    - Modules: 1
    - Services: 86
    - Business Processes: 225
    - Data Entities: 95
    - Business Logic Scripts: 505

    **Key Modules:**
      - metadata

    **System Purpose:**
    Order Care (EOC) manages the complete order lifecycle including:
    - Order capture and validation
    - Order orchestration across multiple systems (DPI, Triad, TC, Pega)
    - Message processing and transformation
    - Provisioning coordination
    - Error handling and recovery
    - Order status tracking and notifications

    **Integration Landscape:**
    - DPI (Digital Platform Integration) - Order submission
    - Triad - Network provisioning
    - TeamConnect (TC) - Dispatch and scheduling
    - Pega - Order management workflow
    - SOAPO - Service activation
    - ESB - Enterprise service bus integration
    

---

## 🔗 Related Documentation

- [Service Catalog](./02-Service-Catalog.md) - Detailed service information
- [Component Map](./06-Component-Map.md) - Component relationships

---

## 📂 Key Directories

Based on the codebase structure, the main directories are:

```
Trunk/FrontierOM/
├── controllers/    - REST endpoints and request handlers
├── services/       - Business logic and orchestration
├── models/         - Data models and DTOs
├── repositories/   - Data access layer
└── integration/    - External system integrations
```

---

**Need implementation details?** Use `get_file_content(path)` with paths from [Service Catalog](./02-Service-Catalog.md).
