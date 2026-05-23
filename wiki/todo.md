todo: lat.md
context:
with regards to this project is that there is much discussion lately about tool sets and workflows to make ai development better, most prodominantly is spec driven development and tools like speckit. There there is persistent memory using tools like Obsidian. There is also the concept of using tools to "index" code bases, as well as documents to assist with lookups, references, and explorations. All of which ultimately assists with token usage reduction.

action:
I initially compared tools like graphify vs codegraph for the act of indexing source and documents, and decided to go with codegraph. but after learning about lat.md and it's usecase, I believe this is the correct tool to use. Update all specs, and wiki docs to include lat.md as the tool used for mapping out the source code, and the wiki documentation, and have it hooked in with the intended workflow of this project.

justification:
lat.md is unequivocally the superior choice because it allows you to build a cohesive blueprint before a single line of code is written. Codegraph relies entirely on analyzing existing code syntax and abstract syntax trees (ASTs)—meaning it is essentially useless until you have a functioning repository to index. By starting with lat.md, you can establish your architectural rules, business logic, and specifications as an intentional, interconnected Markdown knowledge graph. When you finally unleash your AI agent to begin writing code, it won't be guessing your intent based on noisy semantic code searches; it will have a crystal-clear navigation system and structural constraints to follow from day one, with lat check ensuring your new code perfectly matches your pre-planned specs.
