# ProtonVPN Servers API 

> Because deprecated doesn’t mean dead.

After Proton officially **deprecated the ProtonVPN API** developers were left without a clean way to query server data statusand availability.

So… I reintroduced it. 😌  
This project provides a **modern, developer-friendly API** to access ProtonVPN server information again — reliably, programmatically, and without guesswork.

[Visit the documentation](https://carlostkd.ch/proton)


---

## ✨ What Is This?

The **ProtonVPN Servers API** allows you to:

- Fetch **all ProtonVPN servers**
- Monitor **server status and load**
- Distinguish **Free vs Plus (paid) servers**
- Perform **IP ownership checks**
- Receive **offline status notifications**
- Integrate ProtonVPN server intelligence directly into your apps

Whether you're building dashboards, uptime monitors, or automation tools — this API exists so you don’t have to scrape, guess, or cry.

---

## 🔑 Key Features

### 🌍 Server Discovery
- List **all ProtonVPN servers**
- Filter by **country**, **tier**, or **status**

### 📊 Live Server Status
- Online / offline detection
- Server load monitoring
- Identify overloaded or unavailable nodes

### 🆓 vs 💎 Tier Detection
- Instantly see which servers are:
  - Free tier
  - Plus / paid tier

### 🧠 Developer-Friendly API
- Simple REST endpoints
- Predictable responses
- Designed for automation and tooling

### 🔔 Offline Reminders
- Get notified when a server goes offline
- Perfect for monitoring and alerting systems

### 🌐 IP Verification
- Check if an IP address **belongs to ProtonVPN**
- Useful for security tools, analytics, and audits

---

## 🧪 Example Use Cases

- VPN monitoring dashboards
- Server health & uptime tracking
- IP reputation and verification tools
- Custom ProtonVPN clients
- Automation scripts and bots

---

## 🛠️ API Overview

```
GET /api.php?country=all
GET /api.php?country=CH
GET /api.php?city=zurich
GET /api.php?country=CH&city=zurich&include_id=1
GET /api.php?country=US&city=Seattle
GET /api.php?country=CH&include_id=1
```

> Full documentation and response examples are available in the `/docs` folder.

---

## 🚧 Roadmap

- [x] Auto Offline Notifications
- [x] Server Statistics
- [x] IP ownership checks
- [ ] **Lifetime Tier** 👀 (coming soon)

---

## ⚠️ Disclaimer

This project is **not affiliated with Proton AG**.  
All trademarks and brand names belong to their respective owners.

This API is provided for **educational, research, and development purposes**.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

If Proton deprecated the API once, they might do it again —  
so let’s make this one better. 😉

Contact for colaboration/issues  -- Threema: *0001337
---

## ⭐ Support the Project

If this API saves you time, effort, or sanity:
- Star the repo ⭐
- Share it
- Use it responsibly

---


