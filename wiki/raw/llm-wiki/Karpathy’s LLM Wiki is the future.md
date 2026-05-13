---
title: RAG is Dead. Karpathy’s LLM Wiki is the future
source: https://ai.plainenglish.io/rag-is-dead-karpathys-llm-wiki-is-the-future-project-explained-2ae6541616cb
author:
published: 2026-05-02
created: 2026-05-12
description: RAG is Dead. Karpathy’s LLM Wiki is the future | Project Explained A deep-dive into Andrej Karpathy’s viral LLM Wiki concept, and how to apply it to build a real, production WhatsApp AI Bot …
tags:
  - karpathy
  - llm
  - wiki
---
# The Problem with RAG

Clean. Logical. Widely adopted, but here’s the crack nobody wanted to admit.

> When you ask the same question tomorrow? It rediscovers the same answer, the same way, from zero.

There’s no accumulation. No learning. No *memory*.

> *RAG is a librarian who reads every book fresh each morning, with no notes from yesterday.*

**That’s the gap Karpathy saw.** Not a retrieval problem. A *compounding* problem.

## Karpathy’s LLM Wiki: The Big Idea

Karpathy’s fix is almost embarrassingly simple.

Instead of asking your AI to *find* knowledge every time, you ask it to *build* knowledge once and keep building it forever.

He called it an LLM Wiki. A persistent, structured knowledge base that an AI agent actively writes, links, and maintains on your behalf. Not a database. Not a vector store. Just a folder of plain markdown files that gets smarter with every new source you drop in.

The architecture has three layers, and each one has a job.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*0AtibV2iaNfiCeAB.png)

Karpathy’s LLM Wiki: The Big Idea

**The Raw folder** is your inbox. PDFs, articles, research papers, exported notes, web clips – anything goes here. You don’t organise it. You don’t clean it up. You just drop things in and walk away.

**The Wiki folder** is where the magic lives. The AI reads everything in Raw and writes structured, Wikipedia-style pages for every concept, person, project, or idea it finds. These pages cross-link each other using `[[wikilinks]]`, so pulling on one thread surfaces the entire web of related knowledge automatically.

**The Schema file** is the brain’s rulebook. A single markdown file, usually called `CLAUDE.md`, that tells the AI exactly how to write, what tone to use, how to structure each page, and when to update existing entries versus create new ones. It turns a general-purpose LLM into a disciplined, consistent wiki editor.

Here’s the shift that makes this feel like a superpower.

> ***TLDR****; You are no longer maintaining the knowledge base. The AI is. You supply raw material; it builds the structure, draws the connections, and updates everything when new information arrives. Every article you add doesn’t just sit alongside the others. It gets woven into the existing network, making every previous page richer in the process.*

Knowledge stops stacking. It starts *compounding*.

## LLM Wiki vs RAG: The Technical Showdown

Let’s put them side by side and be honest about what each one actually does.

**RAG is stateless. Every query triggers the same pipeline:** retrieve, stuff into context, generate, forget. It works well for simple lookups but starts breaking down the moment your questions get nuanced. **The knowledge never accumulates between sessions because the system was never designed for that.** It was designed for retrieval, not retention.

**LLM Wiki flips the timeline.** The heavy lifting happens *before* you ask anything. The agent reads your sources, synthesizes them into structured pages, and builds the connections upfront. **By the time you ask a question, the answer has already been half-assembled.** Cross-document synthesis isn’t a query-time miracle; it’s baked into the wiki itself.

The setup gap is also worth noting. **RAG needs embeddings, a vector database, a retrieval layer, and an orchestration framework** holding it all together. **LLM Wiki needs a folder and a markdown file locally**. That’s it.

## The Real-World Project: WhatsApp AI Bot with LLM Wiki Brain

Theory is great. But let’s see it actually work.

Meet the [**FreeBirdsCrew WhatsApp AI Bot**](https://github.com/simranjeet97/FreeBirdsCrew_WhatsApp_AI_Bot), a project that takes **Karpathy’s LLM wiki** concept off the whiteboard and wires it directly into WhatsApp. Someone messages you asking about AI agents, career mentorship, or your latest YouTube tutorial. The bot reads your personal wiki, understands the intent, and replies with the exact right link, resource, or guidance. No keyword rules. No vector database. Just structured markdown and a well-prompted LLM doing what it does best.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/0*LiGGIOlPzR9Acdbv.png)

FreeBirdsCrew WhatsApp AI Bot

The bot’s entire brain lives inside a `wiki/` folder. A handful of markdown files cover everything it needs to know: who the person is, which GitHub repos map to which AI topics, which YouTube playlists answer which coding questions, how to handle mentorship requests, and a `SCHEMA.md` that defines the bot's tone, boundaries, and response style. Update a markdown file, and the bot instantly knows something new. No redeployment. No re-embedding. Just save and go.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*MjGgFK3flkS8PUn_CFgdcQ.png)

FreeBirdsCrew WhatsApp AI Bot Architecture

Under the hood, the stack is clean and practical. Node.js and Express handle the backend. `whatsapp-web.js` bridges the WhatsApp connection. Gemini 3.0 Flash powers the AI responses. SQLite quietly logs every conversation. And a React, Vite, and Tailwind dashboard gives you a live view of everything the bot is doing in real time.

The entire project is open source, fully documented, and ready to fork. Swap out the wiki files with your own knowledge and you have a personal AI assistant running on WhatsApp in under an hour.

## [GitHub - simranjeet97/FreeBirdsCrew\_WhatsApp\_AI\_Bot: An intelligent WhatsApp automation bot powered…](https://github.com/simranjeet97/FreeBirdsCrew_WhatsApp_AI_Bot?source=post_page-----2ae6541616cb---------------------------------------)

### An intelligent WhatsApp automation bot powered by Node.js, whatsapp-web.js, and the Gemini AI API. It features an…

github.com

## How to Build Your Own

The best part about this project? You don’t need a PhD, a GPU, or a weekend to get it running. Here’s the entire setup, start to finish.

**Clone the repo and install dependencies.** Split your terminal in two: one for the backend server and one for the React dashboard. Both run independently.

```c
# Terminal 1 — Backend
cd server
npm install
cp .env.example .env
npm run dev

# Terminal 2 — Dashboard
cd frontend
npm install
npm run dev
```
- **Get a free Gemini API key** from [Google AI Studio](https://aistudio.google.com/app/apikey). Paste it inside your `.env` file. The free tier is more than enough to get started.
- **Build your wiki.** Open the `server/wiki/` folder and replace the existing markdown files with your own knowledge. Write about yourself, your projects, your content, and your services. No special syntax. No schema to learn. Plain markdown, the same way you'd write any notes.
- **Edit** `**SCHEMA.md**` to define how your bot should sound. Formal or casual, brief or detailed, whatever it should never say – this single file controls the entire personality.
- **Scan the QR code** that appears in Terminal 1 with your WhatsApp mobile app under Linked Devices. The bot is now live on your number.

Open `http://localhost:5173` to see your dashboard tracking every message in real time.

No vector database. No embeddings. No deployment pipeline. Just markdown files that any non-technical person can open, edit, and save. Updating your bot’s knowledge is literally the same as editing a text file.

> That’s the whole point. The complexity lives in the AI. The knowledge lives with you.

## What You Can Build with This Pattern

The WhatsApp bot is just one interpretation. The pattern itself is far more flexible than any single use case.

**Point it at your SaaS product’s documentation**, and you have a customer support bot that actually understands your product, not just keyword-matches against an FAQ. Feed it your entire work history, past projects, decisions, and lessons learned, and you'll have a personal assistant that knows your professional context better than any colleague does. **Give a PhD student a wiki seeded with their research papers, and it becomes a companion that connects dots across hundreds of sources they’d never link manually.**

**Discord communities can run bots that carry genuine institutional knowledge about the server’s culture, rules, and history**. Recruiters and creators can deploy assistants that know every project, every publication, and every piece of content they’ve ever made — and surface exactly the right one when someone asks.

The wiki is just a folder. What you put inside it determines everything.

## The Bigger Picture: Why This Matters

Step back for a moment and look at what this pattern is actually pointing at.

We’ve spent years building AI tools that are powerful but amnesiac. Every session is a blank slate. Every answer is conjured fresh from training data or retrieved documents that get discarded the moment the conversation ends. **The tools got smarter, but the knowledge never stuck.**

**Karpathy’s insight cuts straight through that.** Compounding knowledge beats repeated retrieval, every single time. It’s the same reason a great engineer with ten years of context outperforms a brilliant graduate on day one. The knowledge that accumulates and connects is worth more than the knowledge that’s merely available.

**Where AI is heading is personal, local, and persistent.** Systems that know *you* specifically, that live on *your* machine, that grow quietly in the background every time you add a new source. Not cloud platforms with your data on someone else’s server. Yours, fully, in plain text files that you can read yourself.

**This isn’t a weekend hack. It’s an early glimpse of what AI assistants will look like when the dust settles.**

## Conclusion

Andrej Karpathy didn’t ship a product. He shared an idea in a GitHub Gist, and that was enough to set off a wave of builders who immediately saw what was possible.

The idea is simple enough to explain in a sentence: stop asking your AI to find knowledge and start asking it to build knowledge. Everything else follows from that shift.

So here’s the question worth sitting with. What would *your* LLM Wiki contain? Your research papers? Three years of meeting notes? Every YouTube video you’ve ever bookmarked? Your company’s entire institutional memory?

Start with one markdown file. Write down what you know about one topic. Let the agent read it, structure it, and link it to the next thing you add.