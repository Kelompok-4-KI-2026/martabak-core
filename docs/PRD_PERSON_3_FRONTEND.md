# 📄 PRD 3: Frontend & UI/UX (Person 3)

* **Target Teammate:** Person 3 (Frontend & UI/UX Developer)
* **Branch to Create:** `feature/frontend-ui`
* **Files to Manage:** `templates/base.html`, `templates/dashboard.html`, `templates/login.html`

---

### **1. Objective**

Build the user-facing web dashboard for **Martabak Core** where franchise partners can upload sensitive franchise data (Personal Data, ID Scans, Secret Recipe Office Documents, and SOP Videos) and select their preferred encryption cipher (**AES, DES, or RC4**).

### **2. Strict Technical Constraints (Assignment Rules)**

* **Scenario Alignment:** Must reflect the "Martabak Core" franchise system styling and data categories (KTP/ID scans, franchise agreements, secret recipes, and kitchen SOP videos).
* **Clear Feedback:** Provide visible confirmation when a file is successfully encrypted, stored, or retrieved.

---

### **3. Implementation Blueprint**

#### **Step A: Base Layout Template (`templates/base.html`)**

This provides a clean, professional dark-mode Tailwind CSS layout for the whole app:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Martabak Core | Franchise Security Vault</title>
    <!-- Tailwind CSS via CDN for rapid agile development -->
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen">
    <nav class="border-b border-slate-800 bg-slate-900 px-6 py-4 flex justify-between items-center">
        <div class="flex items-center space-x-3">
            <span class="text-2xl">🍫🥞</span>
            <span class="font-bold text-xl tracking-wide text-amber-400">Martabak Core Vault</span>
        </div>
        <div class="text-sm text-slate-400">Franchise Security Portal</div>
    </nav>

    <main class="max-w-6xl mx-auto px-6 py-8">
        {% block content %}{% endblock %}
    </main>
</body>
</html>

```

#### **Step B: Dashboard & Upload Form (`templates/dashboard.html`)**

This screen contains the form matching the required data types (`personal_data`, `id_scan`, `office_doc`, `video`) and cipher choices (`AES`, `DES`, `RC4`):

```html
{% extends "base.html" %}
{% block content %}
<div class="grid grid-cols-1 md:grid-cols-3 gap-8">
    
    <!-- Upload Form Card -->
    <div class="md:col-span-1 bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
        <h2 class="text-lg font-semibold text-amber-400 mb-4">🔒 Secure Vault Upload</h2>
        
        <form action="/api/v1/vault/upload" method="POST" enctype="multipart/form-data" class="space-y-4">
            <div>
                <label class="block text-xs font-medium text-slate-400 mb-1">Select Data Category</label>
                <select name="file_type" class="w-full bg-slate-950 border border-slate-700 rounded-lg p-2.5 text-sm text-slate-200 focus:ring-2 focus:ring-amber-500">
                    <option value="personal_data">Personal Data (Franchisee PII)</option>
                    <option value="id_scan">Identity Document Scan (KTP / NPWP)</option>
                    <option value="office_doc">Office Document (Secret Recipe / PDF)</option>
                    <option value="video">SOP Video (Kitchen Masterclass)</option>
                </select>
            </div>

            <div>
                <label class="block text-xs font-medium text-slate-400 mb-1">Choose Encryption Cipher</label>
                <select name="cipher_choice" class="w-full bg-slate-950 border border-slate-700 rounded-lg p-2.5 text-sm text-slate-200 focus:ring-2 focus:ring-amber-500">
                    <option value="AES">AES-256 (Recommended High Security)</option>
                    <option value="DES">DES (Legacy Cipher)</option>
                    <option value="RC4">RC4 (Stream Cipher)</option>
                </select>
            </div>

            <div>
                <label class="block text-xs font-medium text-slate-400 mb-1">Upload File / Media</label>
                <input type="file" name="file" required class="w-full text-sm text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-amber-500 file:text-slate-950 hover:file:bg-amber-400 cursor-pointer">
            </div>

            <button type="submit" class="w-full bg-amber-500 hover:bg-amber-400 text-slate-950 font-semibold py-2.5 rounded-lg transition-colors">
                Encrypt & Store Securely
            </button>
        </form>
    </div>

    <!-- Vault Files List -->
    <div class="md:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
        <h2 class="text-lg font-semibold text-amber-400 mb-4">📂 Franchise Encrypted Vault Registry</h2>
        <div class="overflow-x-auto">
            <table class="w-full text-left text-sm text-slate-400">
                <thead class="bg-slate-950 text-slate-300 uppercase text-xs">
                    <tr>
                        <th class="p-3">Filename</th>
                        <th class="p-3">Category</th>
                        <th class="p-3">Cipher Used</th>
                        <th class="p-3">Action</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-800">
                    <!-- Placeholder row to be rendered dynamically via backend -->
                    <tr>
                        <td class="p-3 font-medium text-slate-200">secret_batter_recipe.pdf</td>
                        <td class="p-3">office_doc</td>
                        <td class="p-3"><span class="bg-emerald-950 text-emerald-400 px-2 py-0.5 rounded text-xs">AES</span></td>
                        <td class="p-3"><a href="#" class="text-amber-400 hover:underline">Download & Decrypt</a></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

</div>
{% endblock %}

```

---

### **4. Acceptance Criteria (Definition of Done)**

* [ ] Pages render cleanly without missing styles using Tailwind CDN.
* [ ] Upload form successfully sends file payloads to FastAPI backend (`/api/v1/vault/upload`).
* [ ] Atomic git commits made during development.