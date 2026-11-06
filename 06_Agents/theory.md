Agents:
- Software systems that use AI to pursue goals and complete tasks on behalf of users. 
- They show reasoning, planning, and memory and have a level of autonomy to make decisions, learn, and adapt.
- Can process multimodal information like text, voice, video, audio, code, and more simultaneously. 
- Can converse, reason, learn, and make decisions; can learn over time and facilitate transactions and business processes. 
- Can work with other agents to coordinate and perform more complex workflows.

1.) Prompt: 
- First thing, we gonna find for an agent is prompt. 
- Examples: 
    - Act as a Research Scientist, Behave as a Doctor, You are supposed to be a SDE-2, Summarize this task etc.
			
2.) Tools: 
- Functions or external resources that an agent can utilize to interact with its environment and enhance its capabilities. 
- They allow agents to perform complex tasks by accessing information, manipulating data, or controlling external systems.
- Can be categorized based on their user interface:
    1.) Physical
	2.) Graphical
	3.) Program-based interfaces. 
- Tool learning involves teaching agents how to effectively use these tools by understanding their functionalities and the context in which they should be applied.

3.) Memory: 
- Agent can maintain context, learn from experiences, and improve performance by recalling past interactions and adapting to new situations. 
- Agents generally have the following kind of memories:
    1.) Short term -> For immediate interactions
	2.) Long term -> For historical data and conversations
	3.) Episodic memory -> for past interactions
	4.) Consensus memory ->  for shared information among agents
			
- Frameworks to built AI Agents / AI Workflows: Langchain, Langraph, CrewAI, Autogen, n8n etc.

Q.) What is the difference between all of these below ?
```
Langchain, LangGraph, Deep Agent, LangSmith, Agent Builder
``` 
-> All the above tools form a layered ecosystem developed by LangChain Inc.
-> They are not competitors; rather, they represent different layers of abstraction and operational tools designed for building, optimizing, and deploying AI applications.

#### 1.) Langchain:
- Open-source framework designed to simplify the creation of applications using large language models (LLMs). 
- It acts as the "glue" that connects LLMs with external data sources, APIs, and databases to build context-aware, reasoning applications. 
- Used For:
    - **Retrieval-Augmented Generation (RAG):** Connecting LLMs to private data sources (PDFs, databases, Notion) so the AI can answer questions based on specific company knowledge.
	- **AI Agents:** Building autonomous assistants that can decide which tools to use (e.g., searching the web, calculating math, or running code) to solve a multi-step problem.
	- **Chatbots & Conversational Interfaces:** Creating advanced chatbots with persistent memory, allowing them to remember past interactions across long conversations.
	- **Data Extraction & Structuring:** Transforming unstructured text (like emails or invoices) into structured JSON formats.
	- **Coding Assistants:** Building tools that interface with repositories to write, review, or debug code.
- It is *productionizable* ?
	- Whether it is productionizable depends entirely on how you use its modern ecosystem.
	- Early versions of LangChain were widely criticized as bloated, fragile, and unsuited for production. However, following the major LangChain v1.0 release, the framework decoupled its core logic into highly stable, production-ready modules. 
	- Today, complex enterprise applications successfully run LangChain in production by heavily leveraging its native enterprise tools, LangGraph (for stateful workflows) and LangSmith (for observability)

#### 2.) LangGraph:
- library used for building stateful, multi-actor applications with LLMs, specifically designed to create complex agentic workflows, cyclic loops, and state-managed architectures.
- fully *productionizable*, explicitly built by LangChain to move LLM applications from simple proof-of-concepts to robust, enterprise-grade production environments.
- Used For:
	- While standard LLM frameworks (like basic LangChain or LlamaIndex) excel at linear, step-by-step pipelines (A → B → C), they struggle with complex, iterative logic. 
	- LangGraph models workflows as graphs (nodes and edges), which makes it ideal for:
		- **Cyclic Workflows & Loops:** Situations where an LLM needs to run a task, evaluate the output, and loop back to fix errors if the results aren't satisfactory (e.g., an agent writing code, testing it, and self-correcting based on compiler errors).
		- **Multi-Agent Architectures:** Breaking down a massive task into specialized agents (e.g., a "Researcher Agent," a "Writer Agent," and a "Critic Agent") that pass messages and collaborate to produce a final result.
		- **Persistent State Management:** Built-in memory systems that automatically save the state of a conversation or task at every single step, allowing for human-in-the-loop approvals, time-travel (rewinding to a previous step), and error recovery.
		- **Streaming Architectures:** Streaming tokens or specific node execution states back to the end-user in real-time, which is crucial for responsive UI/UX.

#### 3.) Deep Agent:
- Architectural pattern and an open-source framework by LangChain designed to handle long-running, multi-step, and complex tasks.
- Unlike traditional "shallow" agents that reactively execute a few tool calls before losing focus or running out of context window space, Deep Agents act more like project managers. 
- These are AI agents designed for complex, long-running work. They combine explicit planning, persistent memory, tool execution, reusable skills, and subagent delegation to decompose tasks, track progress, and act autonomously over time.
- Used For:
	- **Autonomous Software Development:** Navigating complex codebases, multi-file refactoring, writing unit tests, debugging, and resolving failing builds (e.g., LangChain's terminal coding agent, dcode).
	- **Deep Scientific & Market Research:** Autonomously browsing dozens of web or database sources, cross-referencing findings, and synthesizing raw data into comprehensive analyst-level reports.
	- **Complex Document Processing:** Analyzing, auditing, and extracting data from high-volume, multi-format business streams (e.g., enterprise compliance audits, legal contract cross-examination, and financial reconciliation).
	- **Advanced GUI & Computer Automation:** Driving virtual sandboxes to execute terminal commands, orchestrating shell scripts, or using screen visual inputs to interact with desktop applications.
- *Productionizable* but requires a distinct infrastructure strategy compared to standard web applications. Because they are built on top of the stateful *LangGraph* runtime, they natively inherit production-grade features like durable execution, event streaming, and checkpointing, which allow them to survive crashes and resume tasks without starting over.

#### 4.) LangSmith: 
- commercial agent-engineering and LLM observability platform built by the creators of LangChain.
- Unlike LangChain or LangGraph (which are used to actually construct your AI's logic and workflows), LangSmith is used to see inside those workflows. 
- It is completely framework-agnostic, meaning you can use it with LangChain, LangGraph, the Vercel AI SDK, or even pure Python/OpenAI code.
- *LLM observability* : 
	- It is the practice of collecting real-time metrics, traces, logs, and evaluation data from LLM applications to monitor, debug, and improve how they behave in production.
	- Why it matters:
		- Fast Root Cause Analysis: When an AI gives a bad answer, observability lets you look inside the "black box" to see if the failure came from a bad prompt, missing database context, or a model drift issue.
		- Hallucination & Safety Detection: Automated evaluators scan responses in real time for PII leaks, bias, or unsupported claims.
		- Cost & Latency Optimization: It identifies slow bottlenecks or redundant token usage across complex AI chains.
	- Popular platforms used for implementing these practices include tools like Langfuse, LangSmith, and Arize Phoenix.
- LangSmith is highly *productionizable* and is explicitly designed to handle heavy enterprise workload.

#### 5.) Microsoft's Agent Builder:
-  no-code tool integrated directly into Microsoft 365 Copilot that allows everyday business users to create customized, task-focused AI assistants in minutes using natural language.
- Whether Agent Builder is *productionizable* depends entirely on your definition of "production." - If you mean deploying a lightweight, secured, knowledge-based assistant for your internal team or department, yes, it is production-ready out of the box. 
- However, if you mean building complex enterprise-grade automation with strict software engineering life cycles (CI/CD), external API integrations, or public-facing deployment, no, Agent Builder is not designed for that level of production.

### Difference b/w LangGraph and Deep Agents:

##### LangGraph:
- It is **Agent Runtime**.
- **Workflow Design:** Manually declared nodes, edges, and state
- **Best Used For:** Custom multi-agent loops, strict business logic, human-in-the-loop validation gates, and production workflows where you need to explicitly design how state moves.
- **Determinism:** High determinism. You dictate the exact topology, validation gates, and sequence of steps.

#### Deep Agents:
-  It is **Agent Harness** built on top of LangGraph.
- **Workflow Design:** Pre-packaged loop with auto-planning.
- **Best Used For:**  Messy, multi-step, open-ended work (like deep research or coding agents) where you want the model to figure out the workflow rather than coding every graph edge by hand.
- **Built-in Capabilities**: Out of the box, it comes pre-wired with:
	- Planning tools (e.g., dynamic to-do lists and task decomposition)
	- Virtual file systems for persistent memory and context offloading
	- Subagent spawning for isolating parallel or specialized tasks
	- Skills and automated middleware for context management

### Difference b/w Agent Runtime and Agent Harness:

#### Agent Runtime:
- *Infrastructure / Execution* layer that runs, operates, and scales the agent safely in production
- *Primary Question:* "Where and how does the agent run safely and reliably?"
- *Examples:* Temporal, Cloudflare Agents, or Amazon Bedrock AgentCore Runtime

#### Agent Harness:
- also called *Agent scaffolding*.
- *Agent = Model(Brain) + Harness(Environment / Infrastructure)*
- *Application / Orchestration layer* that wraps around a large language model (LLM) to turn it into an active AI agent. 
- *Primary Question:* "How does the agent reason, prompt, and call tools?"
- *Examples:* Custom agent loops, Claude Code, or framework-level harnesses built on top of tools like LangChain.
- *Key Functions:*
	- *Tool Orchestration:* Connects the model to external tools (such as bash terminals, web browsers, compilers, or APIs) so it can execute code or fetch data.
	- *Execution & Feedback Loops:* Runs the model in a continuous loop—calling a tool, capturing the output (like a compiler error or test result), and feeding that result back into the model's next prompt so it can self-correct.
	- *Memory & State Management:* Tracks conversation history, manages durable storage or local file systems, and handles context window limits (through summarization or offloading old data) to prevent "context rot".
	- *Guardrails & Safety Policies:* Enforces permission boundaries, approval workflows, and resource limits so the model doesn’t run infinite loops or execute destructive actions.

### ReAct (Reasoning and Acting) loop :
- Foundational architectural pattern in agentic AI where an LLM alternates between explicit reasoning steps and tool execution.
- Instead of generating a single, "one-shot" answer, the agent operates in a continuous, multi-step cycle typically broken down into three phases:
	1. **Thought:** The model analyzes the current situation and reasons about what to do next (similar to Chain-of-Thought prompting).
	2. **Action:** The model decides to invoke a specific external tool (like a web search, database query, or calculator) with precise inputs.
	3. **Observation:** The system executes the tool, and the raw result is fed back into the LLM's context window as a grounding fact.
- The ReAct loop is the hallmark mechanism of **Shallow Agents**.

### Difference b/w Deep Agents and Shallow Agents:
- Every LLM agent starts the same way: a model calling tools in a loop. Build a weather bot? Easy. Create a code reviewer? Works fine. But try to build an agent that writes a feature across multiple files, runs tests, debugs failures, and iterates—suddenly your simple loop falls apart.
- The difference between ***"shallow agents"*** and ***"deep agents"*** isn't model size or some new, original or previously unused algorithm. It's four architectural choices that enable agents to handle complex, multi-step tasks over longer time horizons.
- A good example of a Shallow agent is: "Let's say you called customer service and got stuck talking to a robot that couldn't understand what you really needed. That frustrating experience is what we call a 'shallow agent.'
- ***Shallow Agents:***
	- A shallow agent is just an LLM calling tools in a loop with no planning, memory management, or task delegation. The basic pattern—receive prompt, call tools, repeat—works until:
		- **Context explodes:** Your agent's 20th tool call returns 5,000 lines of logs. Now every subsequent LLM call costs more and performs worse as the context fills with noise.
		- **Tasks compound:** Ask your agent to "analyze user feedback and update docs accordingly." Without explicit decomposition, it might search feedback, get overwhelmed by volume, and lose track of the documentation update entirely.
		- **Memory vanishes:** Your agent finds critical info in step 3 but forgets it by step 8 because the context is flooded with intermediate outputs.
		- **Retries thrash:** A subtask fails. The agent tries again with the entire conversation history, making the same mistake because it can't isolate and focus.
	- These aren't LLM limitations—they're architecture limitations. Production agents solve them with scaffolding around the basic loop.
	- Operates on the simplest possible architecture; follows a basic loop based design.
	- Basic Cycle of Shallow Agents:
		- Step 1: Receive your prompt
		- Step 2: AI figures out what to do  
		- Step 3: Calls the necessary tool  
		- Step 4: Observes the result 
		- Step 5: Repeats until done 
	- Think of it like this: you ask 'What's the weather in Mumbai?' The agent reads your question, realizes it needs to call a weather API, gets the data, and responds 'It's 28 degrees and sunny.' Simple, fast, and effective. 
	- Shallow agents are fundamentally **reactive**. They respond to what's happening right now, in this moment. They don't look ahead or plan for the future.There’s no real LLM planning and reasoning involved; only immediate responses based on the current input. 
	- This reactive model works brilliantly for quick requests and is still widely used in Voice AI agents for customer service today. The problem starts when tasks get complicated. 
	- Shallow Agents memory is ***ephemeral*** meaning it *disappears* quickly. Once the conversation gets long or the task requires many steps, they start forgetting things
	- Information gets pushed out of their limited memory window, and they lose track of what they were doing. 
	- **When Shallow Agents Work Well:**
		- Ideal for simple, repetitive workflows and basic AI agents for business automation.
		- Pizza Hut used shallow agents for order tracking. When customers wanted to know 'Where's my pizza?', the agent would: 
			- 1. Recognize keywords like 'order', 'pizza', 'where', 'status'  
			- 2. Ask for order number  
			- 3. Look up order in database  
			- 4. Return pre-formatted response: 'Your order #12345 is out for delivery, estimated arrival 25 minutes' 
		This worked beautifully because the task is straightforward. There's one question (where's my order?) and one answer (here's the status). No complexity, no special cases. 
	- **When Shallow Agents Fail/Break:**
		- *Example of Shallow Agents Failing:* "A major bank tried using shallow agents for customer complaints. This is where limitations became obvious, especially in areas like AI productivity measurement, where task success isn’t 100% complete (success) or completely unfinished(failed)."
			- Customer: 'I was charged twice for the same transaction, and now my account is overdrawn. I never authorized this second charge, and I'm getting hit with overdraft fees. This is the third time this month!' 
			- The shallow agent saw the keyword 'charged' and responded: 'I can help you review your recent charges. Please log into your account to see your transaction history.' 
			- The customer already knew about the charges - that wasn't the problem! They needed:
				- The duplicate charge reversed  
				- Overdraft fees waived 
				- An explanation for why this keeps happening 
				- Assurance it won't happen again 
			- The shallow agent couldn't understand this multi-part problem. It kept giving generic responses until the frustrated customer demanded a human representative. The bank found that 78% of complaints handled by their shallow agent ended with escalation to humans anyway. 
- ***Deep Agents:***
	- Represent the next evolution in Autonomous AI Agents; emerged as a solution to the limitations of shallow agents. 
	- They're called 'deep' because they can dive deep into complex topics and work on them for extended periods - hours or even days. 
	- Deep agent understands the complete problem context. 
	- They create and follow a systematic plan. If require, they delegate work to specialists who handles specific tasks.
	- They take multiple coordinated actions simultaneously; stores everything in files for future reference. 
	- Most importantly, it solved everything without human intervention. 
	- *Core difference b/w Deep and Shallow:* 
		- Deep agents don't just react. 
		- They plan ahead, organize their work, delegate tasks to specialists, and maintain persistent memory outside their conversation window. 
		- This is what people mean when they talk about building autonomous AI agents. 
		- While shallow agents are like someone working without a to-do list, constantly distracted and forgetting things, deep agents are like organized project managers who write down their plan, assign work to team members, keep notes in files, and systematically work through complex projects. 
	- **How Deep Agents Solve the Problems ?**
		- Let's see, how Deep Agents solves the frustrated customer experience a customer had because of shallow agents.
		- Customer: 'I was charged twice for the same transaction, and now my account is overdrawn. This is the third time this month!' 
		- **Step 1:** Deep agent creates a written plan listing search for duplicate charges, find previous fraud reports, calculate total refund, process reversals, identify root cause, implement prevention, respond to customer.   
		- **Step 2:** Assigns specialized work. Data specialist searches and finds the $500 duplicate plus two December incidents totaling $1,500. Finance specialist processes the full $1,500 reversal with 24-hour timeline. Security specialist discovers the card was compromised and recommends immediate replacement.   
		- **Step 3:** All findings, actions, and timelines get saved to external files so nothing is forgotten even if the conversation gets long.   
		- **Step 4:** Following detailed procedures for fraud cases, agent ensures immediate reversal, clear explanation, specific timeline, prevention setup, and written confirmation.   
		- **Step 5:** Agent gives complete response covering all three reversed charges, 24-hour refund timeline, new card arriving in 3 days, transaction alerts activated, and detailed report sent via email. 
	- **How Deep Agents Actually Work ?**
		- Deep agents are built on four architectural pillars that define modern Agentic AI System Architecture:
			- 1.) ***Planning Tool:***
				- Agent doesn't just think about its plan - it writes it down in a file, like a to-do list. 
				- After every action, it reviews and updates this plan, marking items as pending, in progress, or completed. 
				- When something fails, it adapts the plan instead of blindly retrying. This keeps everything focused on the main goal. 
			- 2.) ***Sub Agents:*** 
				- Specialist sub-agents. 
				- Complex work gets broken into focused pieces. 
				- A main coordinator assigns each piece to a specialist - maybe a researcher, a coder, or a writer. 
				- Each specialist runs its own loop, handles its own errors, and returns clean results. The coordinator then stitches everything together and moves forward. 
			- 3.) ***File System:*** 
				- External file system. 
				- Instead of keeping everything in conversation memory, the agent writes to actual files and databases. 
				- Code goes in one file, research notes in another, analysis in a third. Later steps can read exactly what they need. 
				- This memory persists forever and doesn't disappear when the conversation gets long. 
			- 4.) ***System Prompt:*** 
				- Detailed instructions. 
				- The agent follows comprehensive guidelines covering when to stop and plan, when to use a specialist, which tools to use in what situations, how to organize files, and when to ask humans for help. 
				- Generic prompts like 'be helpful' don't work anymore - these agents need explicit operating manuals. 
		- *Example:* **"Market Research Report"**
			- **Someone needs:** *Comprehensive analysis of the electric vehicle market for investment decisions.* 
			- 1.) *Planning Tool:* Research plan covers gathering sales data, identifying key players, analyzing growth patterns, assessing risks, building projections, and writing the report. 
			- 2.) *Sub Agents:* Tasks get assigned to specialists - researcher collects data from 15 global markets, analyst identifies a 34% growth trend, financial specialist creates 5-year projections, writer drafts professional content, editor polishes everything. 
			- 3.) *File System:* All work saves to organized files including raw data, analysis notes, financial models, and the final report. Quality requirements mandate source citations, visual charts, professional formatting, and fact verification. Specialists update shared status as they progress. In 3-4 hours, a complete 45-page investment report with data, visuals, and recommendations is ready. 
			- 4.) *System Prompt:* You are an autonomous multi-agent market research system. When a user requests a market research report, create a structured research plan, divide the work into specialized tasks, and delegate them to expert sub-agents such as market researchers, data analysts, financial analysts, report writers, and quality reviewers.
		- *Code Example:*
		```
		class TaskAgent:
			def __init__(self):
				self.system_prompt = load_detailed_instructions()
				self.tools = [
					# Core execution
					read_file, write_file, edit_file,
					run_command, search_code,

					# Planning & tracking
					track_plan, update_progress,

					# Delegation
					spawn_subagent, wait_for_agent,
				]

			def run(self, task):
				# Agent decomposes task using track_plan
				# Uses file tools to manage large outputs
				# Spawns sub-agents for distinct subtasks
				# Each sub-agent has tailored prompt + tools
				pass
		```
		- Loop is still simple: generate → call tools → repeat. 
		- But the tools enable: 
			- ***Persistence*** through file operations.
			- ***Decomposition*** through planning tools
			- ***Focus*** through sub-agent delegation.
			- ***Reliability*** through detailed prompts.
		- **When to Add complexity:**
			- Start with the simplest agent that could work. Add layers only when you hit limits:
				- Agent losing track of multi-step tasks? → Add planning tools
				- Context blowing up? → Add file system tools
				- Single subtask consuming all the context? → Add sub-agent spawning
				- Agent making preventable mistakes? → Extend system prompt with examples


---------------------------------------------------------------------------------------------------

### Generative AI Frameworks
	• Purpose: Focused on prompting, managing large language models (LLMs), connecting data sources (like RAG/Retrieval-Augmented Generation), and handling reactive text, image, or code generatio
	• How They Work: They wait for a direct user prompt, process it through a model, and return a generated output (e.g., writing an email, summarizing a PDF, or generating an image).
	• Key Components: Prompt templates, vector database connectors, simple memory buffers, and model wrapper APIs.
	• Examples: Basic implementations of LangChain (for standard chain workflows), LlamaIndex (for data indexing), Haystack, and DSPy.

### Agentic AI frameworks
	• Purpose: Built to create autonomous or semi-autonomous AI agents that can plan multi-step workflows, reason, make decisions, use external tools/APIs, and loop through actions until a goal is achieved.
	• How They Work: Instead of just answering a question, an agentic framework gives an LLM a high-level objective. The agent perceives the environment, breaks the goal into tasks, executes tools, evaluates the results, and iterates (Perceive → Reason → Plan → Act → Reflect).
	• Key Components: State management (tracking progress across steps), long-term/short-term memory, tool-calling interfaces (APIs/databases), and multi-agent orchestration.
	• Categories & Examples:
		1.) Stateful & Graph Workflows: LangGraph (for branching and cyclic agent logic).
		2.) Multi-Agent & Role-Based Systems: AutoGen and CrewAI (where multiple specialized AI agents talk to each other to solve a task).
		3.) Enterprise Orchestration: Microsoft Semantic Kernel.
		4.) Prototyping UIs: Langflow and Flowise

**Q.)** *Can we built a RAG system us Agentic AI or Agentic AI frameworks ? How is it different from RAG systems built using Generative AI ?*

**Ans.)** Yes, We can build an Agentic RAG system using Agentic AI and popular agentic frameworks.

- Unlike traditional RAG which follows a rigid, linear sequence (embed query -> retrieve top-k documents -> generate answer), *Agentic RAG* wraps the retrieval process in an autonomous reasoning loop. 
- An AI agent dynamically decides when, what, where, and how many times to retrieve information, checks if the retrieved data is actually sufficient, rewrites queries, or falls back to web searches or external APIs if needed.
- Popular Frameworks to Build Agentic RAG: LangGraph & LangChain, LlamaIndex, Agno (formerly Phidata), CrewAI etc.
- ***Note:*** Agentic RAG systems are slower and incur higher token costs than classic RAG because they involve multiple LLM calls and reasoning loops.