# Product Requirements Document (PRD): Replate Multi-Channel Platform

## 1. Executive Summary
Replate is a logistics platform designed to eliminate food waste by connecting donors (businesses) with volunteer drivers and NPOs. This document outlines the phased rollout of the platform, moving from a core CLI tool to a multi-channel system integrated with the WhatsApp Business API.

## 2. User Stories
*   **As a Volunteer Driver**, I want to easily discover and claim available food pickups near me so that I can efficiently rescue food and deliver it to people in need.
*   **As a Food Donor (Restaurant/Cafeteria Manager)**, I want to report surplus food quickly via WhatsApp without installing a new app, so that it doesn't go to waste during my busy shift.

## 3. Version 1: Core Operations & Lead Generation (CURRENT)

### 3.1 V1 Success Metrics
*   **Engagement:** > 80% of reported WhatsApp donations successfully converted into claimed tasks.
*   **Efficiency:** Average time from "WhatsApp message received" to "Task available in CLI" under 5 minutes.
*   **Volume:** Capture at least 10 new donation leads via the WhatsApp channel in the first month.

### 3.2 V1 Scope: Driver Operations (Python CLI)
*   **Authentication:** Simulated login/signup for prototype testing with local session persistence.
*   **Onboarding:** Guided NPO partner selection for new drivers.
*   **Task Discovery:** Browse available pickups for Today/Tomorrow, ranked by Haversine distance.
*   **Task Execution:** Atomically claim tasks and log completion (weight, photo simulation, and destination).

### 3.3 V1 Scope: WhatsApp Lead Generation
*   **Automated Intake Bot:** A conversational interface for donors to report surplus food.
*   **Multi-Turn Interaction:** Capture identity, location, food description, quantity, and pickup window.
*   **Smart Categorization:** Automatically transform natural language (text) into structured database categories using AI.

### 3.4 V1 Non-Goals
*   **Production Auth:** We are not implementing real JWT/signed-token auth in V1 (Simulated only).
*   **Real Image Uploads:** Photo confirmation is simulated; we are not yet storing binary image data in Supabase.
*   **Automated Dispatch:** We are not sending proactive alerts to drivers yet (Pull-model only).

---

## 4. WhatsApp Driver Experience — Build Status

### 4.1 WhatsApp vs. React Native App

| Feature | React Native App | WhatsApp V1 |
|---|---|---|
| **Auth** | Full signup/login/forgot password/reset | Phone number = identity, no login |
| **Onboarding** | NPO partner selection on signup | Not built |
| **Task list** | Filtered by date, Today/Tomorrow toggle | Chat bot reply (planned, not built) |
| **Distance sorting** | Tasks sorted by proximity | Not built |
| **Task detail** | Full detail — contact, access instructions, map | Task Detail Flow (built) |
| **Maps** | Opens Apple/Google Maps | Address as text (tappable link) |
| **Claim task** | Atomic claim with conflict handling | Flow submission handler (built) |
| **Log completion** | Weight + NPO selection + notes + photo | Not built |
| **Mark as missed** | `submitTaskMissed` API call | Not built |
| **My Tasks** | Active claimed tasks list | Not built |
| **My Account** | Profile, NPO partner, logout | Not built |
| **Photo upload** | Native camera, stored in Supabase | **Not possible in Flows** |

### 4.2 Remaining WhatsApp Driver Features (Prioritization Backlog)

| Gap | How to build in WhatsApp |
|---|---|
| Completion logging | Flow with weight, NPO dropdown, notes fields |
| My Tasks | Chat bot — driver texts "my tasks", bot replies with list |
| Task list browsing | Chat bot — driver texts "tasks", bot replies with numbered list |
| Driver registration | Multi-screen Flow — name, email, NPO selection |
| Distance sorting | Backend sorts by Haversine before sending bot reply |
| Mark as missed | Chat bot — driver texts "missed", bot asks which task |
| My Account | Chat bot — driver texts "account", bot replies with profile |

> **Note:** Photo upload is the only feature that cannot be built with WhatsApp Flows. All other gaps are a matter of prioritization.

---

## 5. Version 2: Proactive Coordination & Impact (ROADMAP)
*   **Proactive Volunteer Dispatch:** Automated WhatsApp alerts to the nearest 3 drivers for high-priority tasks.
*   **Donor Impact Loop:** Automated gratitude messages with impact metrics (e.g., "You provided 25 meals").
*   **Live Support:** Human-in-the-loop escalation for on-the-ground issues.

---

## 5. High-Level Requirements
*   **Multi-Channel Entry:** Support both CLI (drivers) and WhatsApp (donors).
*   **Scalable Persistence:** Use a cloud-based BaaS (Supabase) to centralize data across channels.
*   **AI-Enabled Logistics:** Use LLMs to minimize manual data entry for donors.

---

## 6. Reviewer Checklist
- [ ] Do the success metrics accurately reflect the value of the WhatsApp integration?
- [ ] Are the boundaries between V1 (Pull-model) and V2 (Push-model) clear?
- [ ] Does the "Donor User Story" justify the choice of WhatsApp as the primary intake channel?
