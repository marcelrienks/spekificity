The Karpathy Approach
Then I read Andrej Karpathy’s post about using LLMs to build personal knowledge bases. His approach is elegant:

1. Ingest raw sources (articles, papers, repos, notes) into a `raw/`directory
2. Compile them with an LLM into a wiki — a collection of interconnected `.md` files
3. Query the wiki by asking the LLM complex questions against it
4. File back the answers and explorations into the wiki, so it always grows

The critical shift: you rarely touch the wiki directly. It’s the LLM’s domain. Your job is to feed it sources and ask questions. The LLM organizes, cross-links, and maintains everything.

I realized I was sitting on 8 months of raw source material. It was already in markdown. It just needed compilation.