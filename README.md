Here’s a corrected version of your README.md with proper Markdown syntax and code block handling. I fixed issues like improperly nested lists inside code blocks, missing code block closures, and headings/sections that were not properly separated. I also cleaned up some minor formatting inconsistencies:

# Aegis: Your AI Security Guardian for Cardano

**Project Status: Actively Developed | Funded by the Cardano Community in Fund14**

Aegis is an open-source project building an AI-powered security assistant to help users and developers identify scams, understand transactions, and protect their assets on the Cardano blockchain. Our goal is to make the Cardano ecosystem the safest place to operate in Web3.

**Official Website:** [**aegis-cardano.vercel.app**](https://aegis-cardano.vercel.app/)  
**Catalyst Proposal:** [**View Our Proposal**](https://bit.ly/aegiscardano)

---

## Connect With Us
* **X (Twitter):** [@aegiscardano](https://x.com/aegiscardano)
* **Telegram:** [Aegis Cardano Community](https://t.me/aegiscardano)
* **YouTube:** [Bana Codes Channel](https://youtube.com/@BanaCodes)

---

## The Problem
The fear of scams is a major barrier to mass adoption. As the Cardano ecosystem grows, users are increasingly exposed to sophisticated phishing attacks, malicious dApps, and confusing transactions designed to drain their wallets. This creates a climate of fear that slows down growth and hurts user trust.

---

## Our Solution
Aegis provides a free, intelligent, and easy-to-use security layer for everyone. We are developing an **open-source security API** that any Cardano developer can integrate into their applications.

To demonstrate its power and provide immediate value, we're also building a free public **Telegram and Discord bot** that offers:

* **AI Link Scanner**: Analyzes websites for signs of phishing or wallet drainers.
* **Address Reputation Check**: Scans wallet addresses for suspicious on-chain activity.
* **Asset Authenticity Verification**: Confirms if an NFT or token is genuine by checking its Policy ID.
* **Plain-Language Transaction Explainer**: Translates complex transaction data into a simple, human-readable summary *before* you sign.

---

## How Aegis Works
```mermaid
graph TD
    A[User on Telegram/Discord] -- Sends Link/Address/Tx --> B(Aegis Bot)
    B -- Analyzes Request --> C{Aegis Core API}
    C -- Gets On-Chain Data --> D[Cardano API: Koios/Blockfrost]
    C -- Performs AI Analysis --> E[AI Model API: LLM]
    C -- Returns Simple Result --> B
    B -- Sends Clear Warning/Explanation --> A
```

---

Bot Commands (In Development)

Here's a preview of how you'll interact with the Aegis guardian bot:

Check a Wallet Address

/check_address addr1q8...

Aegis Reply: ⚠️ Caution! This address was created 3 hours ago and has interacted with a known scam contract.

Scan a Link

/scan_link https://suspicious-minswap.io

Aegis Reply: 🚨 High Risk! This website appears to be a phishing site impersonating Minswap. Do not connect your wallet.

Explain a Transaction

(User pastes a raw transaction hex)

Aegis Reply: In simple terms, this transaction will: Send 50 ADA to an unknown wallet and give a smart contract permission to spend ALL of your SpaceBudz NFTs.


---

Project Vision

Our vision is to build a foundational trust layer for Cardano. By providing developers with a powerful, open-source security toolkit, we can collectively make the entire ecosystem safer, encouraging new users to join with confidence and empowering developers to build more secure applications.

---

Roadmap (Updated Sept 2025)

Phase 1 (Months 1-3): [██████████] 100%

[x] Set up public GitHub repository with MIT License. (Completed)

[x] Develop core bot framework for Telegram and Discord. (Completed)

[x] Integrate with Cardano blockchain APIs (Blockfrost/Koios). (Completed)

[x] Launch initial features: Address Reputation & Asset Authenticity. (Completed)


Phase 2 (Months 4-6): [███░░░░░░░] 30%

[x] Integrate AI model for the Link Scanner feature. (In Progress)

[ ] Develop and test the Plain-Language Transaction Explainer.

[ ] Publish comprehensive API documentation for developers.

[ ] Launch public beta and gather community feedback.




---

Development Philosophy

Aegis is built using a modern, AI-augmented development philosophy. By pairing an experienced developer's intuition with advanced AI coding agents, we can achieve rapid, secure, and robust development. This human-AI collaborative approach allows us to focus on high-level security architecture while ensuring the code quality remains exceptionally high.


---

Get Involved

This project is for the community, by the community. We are proudly funded by the Cardano community through Project Catalyst Fund14 — thank you for your trust and support!

Follow our Progress: Star and watch this repository for real-time updates.

Contribute: We welcome contributions! Please check our open issues for tasks, especially those tagged good first issue.

Join the Community: Participate in the conversation on Telegram and follow the development journey on YouTube.
