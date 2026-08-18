# AI Scope and Handoff

## Latest functional baseline

### 1. Consumer Demand Clustering

Consumer demand is embedded and grouped into similar demand Clusters. Vector DB retrieval is the default approach. If semantic similarity alone is insufficient, combine category, price, quantity, product attributes, and other backend-provided fields through Hybrid logic.

### 2. Demand Cluster–Seller Matching

Retrieve Seller Offer candidates using embeddings. Apply structured filtering, scoring, and ranking when needed. The final match must be reproducible and must not be an arbitrary LLM decision.

### 3. Seller-facing Demand Analysis

Analyze Cluster and consumer data to expose requirements, preferred price ranges, demand size, condition distributions, common characteristics, benefits, risks, and considerations. Numeric claims must come from actual aggregation. An LLM may explain computed results in natural language but must not invent facts.

### 4. Post-match Consumer RAG Chatbot

After matching, consumers can ask about the matched seller's product and terms. Retrieval is restricted to information provided by that seller. Unsupported answers must abstain with a clear “not found in seller-provided information” response.

## Explicitly out of scope

- Consumer/Seller natural-language intake and LLM ping-pong
- Treating a fixed Consumer/Seller Schema as an AI-owned contract
- Mandatory importance weights
- Qwen3-8B-AWQ + always-on vLLM as a fixed architecture

The model and serving architecture must be selected against the four functions and their evaluation results.
