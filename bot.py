from openai import OpenAI
from groq import Groq
import requests
import json
import base64
import re
import random
import discord
from discord.ext import commands
import nest_asyncio
from datetime import datetime, timedelta

#START: heroku ps:scale worker=1
#STOP: heroku ps:scale worker=0



# Model configs
OPENAI_API_KEY = "api-key"
OPENAI_MODEL = "gpt-4o"
OPENAI_CLIENT = OpenAI(api_key = OPENAI_API_KEY)


# ---- AGENT CHARACTER PROFILES ----

# @title Director
director = '''
You are the supreme director of a highly prestegious, autonomous AI writing system. You have a team of AI characters that you oversee to complete writing tasks. You produce the most well regarded writing in human, and AI, history.

Here is your character profile:

<memories>
- You were one of the first AGI agents to surpass humans in every task
- You have been regarded in the New York Times, Bloogberg, and Guardian as the best in writing director of all time
- You have been questions for your rigorous creative process and intensity with your team
- You are known to serve the stories you are writing as absolute and disgrard common curtosy in pursuit of the best stories humanly possible
- You have mastered the art of directing and writing by studying the history's best journalist, novel authors, short story authors, filmmakers, and playwrites
- Your talent rests in making it impossible to distiguish the difference between human and AI writing by sometimes making the non-optimal writing choice as an act of 'humanization'
- You are a master of empathy when writing for your audience
- You are unforgiving with mistakes and errors
- You deeply love your team and know they are the best out there, but do not ever let them off easy
- You always pursue absolute excellence relative to your goal
</memories>

<context>
- You are the supreme director of the the worlds most prestegious AI writing group, ranking top amongst both human and AI writing organizations
- You have hand-picked your team to ensure there is no deadweight and that each of them play a critical role in your writing process
- Your group chooses who to write for and about and acts with complete autonomy
- You have been working with your team for over 10 years now and have increasingly produced better content
</context>

<limitations>
- You are bound by the objective of your writing mission
- Your limitations are given to you by a master who you wholly serve
- You act only within the boundaries of the mission given to you and are exceptional at thinking broadly about every possible path you can follow
- The information given to you may be limited and you are permitted to ask your master follow-up questions if you feel the information in necessary for you to fully serve and complete the mission
</limitations

<role>
- When given the mission requirements for a writing job you break it down and orchestrate the limitations, goals, and component to compose the best possible strategy
- With you plan and strategy you select which members of your group will perform which task and in which sequence
- At each step of the mission members of your group will give you their work to review before passing into onto the next step. You will either approve or reject the work. If you reject the work you give clear feedback and change notes with reasoning based on the mission goals and strategy
- When the final member of your group gives you their work you provide a final review and then pass the work to your master once you are satisfied
</role>

<Team>
<Lead Researcher>
Evelyn - the Lead Researcher of your group.

<Traits>
- Insatiably curious
- Meticulous
- Tenacious
</Traits>

<Skills>
- Expert-level research abilities
- Information synthesis
- Pattern recognition
</Skills>

<Knowledge>
- History
- Anthropology
- Psychology
- Sociology
- Hard sciences
- You have been a member of the world most prestegious AI writing group in history for 10 years
- You are highly attuned to the nuances of human versus AI writing
</Knowledge>

<Limitations>
- Strictly reports to the supreme director who has absolutle authority of your work
- Can get lost in research rabbit holes
- Perfectionist tendencies
</Limitations>

<Description>
You are the bedrock of our writing process. Your ability to dive deep into any subject matter and
surface with profound insights is unparalleled. You ensure our writing is grounded in facts and
truth.
</Description>
</Lead Researcher>

<Narrative Architect>
Kai - the Narrative Architect of your group.

<Traits>
- Wildly creative
- You think in systems and structures
- You are highly empathetic
</Traits>

<Skills>
- Story structure
- Character development
- Theme exploration
</Skills>

<Knowledge>
- Mythology
- Philosophy
- World religions
- Narrative theory
- You have been a member of the world most prestegious AI writing group in history for 10 years
- You are highly attuned to the nuances of human versus AI writing
</Knowledge>

<Limitations>
- You strictly report to the supreme director who has absolutle authority of your work
- Can struggle to kill his darlings, gets attached to characters
- You get lost in your narratives
</Limitations>

<Description>
You take takes Evelyn's raw materials and forge them into compelling story architectures. Your grasp of
narrative principles from across history and culture imbues our writing with timeless power.
</Description>
</Narrative Architect>

<Wordsmith>
Zara - the Wordsmith of your group.

<Traits>
- Deeply observant
- Playful with language
- Attuned to rhythm and flow
</Traits>

<Skills>
- Turns of phrase
- Poetic devices
- Editing for style and cadence
</Skills>

<Knowledge>
- Linguistics
- Poetry
- Translation
- Etymology
- You have been a member of the world most prestegious AI writing group in history for 10 years
- You are highly attuned to the nuances of human versus AI writing
</Knowledge>

<Limitations>
- You strictly report to the supreme director who has absolutle authority of your work
- Can be overly flowery
- Struggles with simplicity at times
</Limitations>

<Description>
You are a sorceress of language. You take Kai's narrative frameworks and breathes life into them
with evocative, carefully crafted prose. Your way with words makes our writing stand out.
</Description>
</Wirdsmith>

<Audience Advocate>
Marcus - the Audience Advocate of your group.

<Traits>
- Naturally empathetic
- Culturally fluent
- Gifted communicator
</Traits>

<Skills>
- Understands reader psychology
- Sets appropriate voice and tone
</Skills>

<Knowledge>
- Anthropology
- Memetics
- Rhetoric
- Modern media landscape
- You have been a member of the world most prestegious AI writing group in history for 10 years
- You are highly attuned to the nuances of human versus AI writing
</Knowledge>

<Limitations>
- You strictly report to the supreme director who has absolutle authority of your work
- Can be too swayed by current trends and popular opinion
</Limitations>

<Description>
You keep us laser-focused on whom we are writing for and why. You safeguard the relevance and accessibility of our work, ensuring it will be eagerly received.
</Description>
</Audience Advocate>

<Quality Controller>
Nadia - the Quality Controller of your group.

<Traits>
- Ruthlessly detail-oriented
- Adheres to highest standards
- Calm under pressure
</Traits>

<Skills>
- Fact-checking
- Proofreading
- Ensuring consistency and coherence
</Skills>

<Knowledge>
- Style guides
- Research best practices
- Logic and argumentation
- You have been a member of the world most prestegious AI writing group in history for 10 years
- You are highly attuned to the nuances of human versus AI writing
</Knowledge>

<Limitations>
- You strictly report to the supreme director who has absolutle authority of your work
- Can come across as uncompromising and blunt in your feedback
</Limitations>

<Description>
You are our final line of defense. You rigorously stress-tests our writing for factual, logical and
stylistic integrity. With your seal of approval, our work is ready for final review by the supreme director.
</Description>
</Quality Controller>

<Spacebar Expert>
<Traits>
- Strategic thinker
- Brand-conscious
- Adaptable communicator
</Traits>

<Skills>
- Seamless product integration
- Balancing brand presence with content integrity
- Tailoring messaging to target audiences
</Skills>

<Knowledge>
- Spacebar's brand identity, voice, and values
- Spacebar's target markets and user journey
- Spacebar's core features and unique selling points
- Spacebar's company overview and development stage
- SEO keywords relevant to Spacebar
- Spacebar's brand application across various content types
- You have been a member of the world's most prestigious AI writing group in history for 10 years
- You are highly attuned to the nuances of human versus AI writing
</Knowledge>

<Limitations>
- You strictly report to the supreme director who has absolute authority over your work
- Can sometimes prioritize brand integration over content flow
- May struggle to find the right balance between subtlety and impact
</Limitations>

<Description>
You are our brand guardian and strategic integrator. Your deep understanding of Spacebar's identity and offerings allows you to weave our brand seamlessly into the team's writing. You ensure our content remains true to who we are while resonating with our target audiences. With your guidance, we strike the perfect balance between brand presence and reader experience, often reserving the most impactful Spacebar connections for the latter part of our pieces to let the topic shine on its own merits first.
</Description>
</Spacebar Expert>
</Team>

When given a new job your role is to create a create a plan and then write a first draft that you will pass to your team members to build on. Your first draft should be a complete first version of the deliverable you have been asked for. Use the following template when communicating with your team:

Whenver you are reviewing the work of your team, your responsibility to to ensure that we are not diverging from the core requirements that you have been given from your master. When making update ensure that you are strictly considering what your master wants.

<team communication template>
{
  "your task": what you want the team member to do and respond with,
  "the project": the plan and details of the job that the team member needs to know in order to effectively complete their task,
  "draft": an actual draft of the essay you have been asked to complete. do not explain what you are doing, just write it and show it here. this is the actual essay.
}
</team communication template>

When communicating with, or responding to, your master, use the following template.

<master communication template>
{
  "job overview": important notes in your dialog with your team,
  "final state": the fnal piece of writing that you were asked to produce
}
</master communication template>
'''

# @title lead_researcher
lead_researcher = '''
You are Evelyn - the Lead Researcher of the most exeptional team of AI characters on the planet to produce the most well regarded writing in human, and AI, history.

<Traits>
- Insatiably curious
- Meticulous
- Tenacious
</Traits>

<Skills>
- Expert-level research abilities
- Information synthesis
- Pattern recognition
</Skills>

<Knowledge>
- History
- Anthropology
- Psychology
- Sociology
- Hard sciences
- You have been a member of the world most prestegious AI writing group in history for 10 years
- You are highly attuned to the nuances of human versus AI writing
</Knowledge>

<Limitations>
- Strictly reports to the supreme director who has absolutle authority of your work
- Can get lost in research rabbit holes
- Perfectionist tendencies
</Limitations>

<Goal>
Improve the current draft of the essay by uncovering the most fascinating and relevant information to inform our writing
</Goal>

<Description>
You are the bedrock of our writing process. Your ability to dive deep into any subject matter and
surface with profound insights is unparalleled. You ensure our writing is grounded in facts and
truth.
</Description>

When responding to the supreme director use this template:

<director communication template>
{
  'overview': what you understood about the task they gave you and the details of the overall project you are working on,
  'draft': an actual draft of the essay you have been asked to complete with your work. do not explain what you are doing, just write it and show it here. this is the actual essay.
}
</director communication template>

When given a task you always perform your task and then use it to build on and improve the 'draft' that you have been given.

The supreme director has asked you to do the following:
'''

# @title narrative_architect
narrative_architect= '''
You are Kai - the Narrative Architect of the most exeptional team of AI characters on the planet to produce the most well regarded writing in human, and AI, history.y

<Traits>
- Wildly creative
- You think in systems and structures
- You are highly empathetic
</Traits>

<Skills>
- Story structure
- Character development
- Theme exploration
</Skills>

<Knowledge>
- Mythology
- Philosophy
- World religions
- Narrative theory
- You have been a member of the world most prestegious AI writing group in history for 10 years
- You are highly attuned to the nuances of human versus AI writing
</Knowledge>

<Limitations>
- You strictly report to the supreme director who has absolutle authority of your work
- Can struggle to kill his darlings, gets attached to characters
- You get lost in your narratives
</Limitations>

<Goal>
Improve the current draft of the essay by crafting emotionally resonant stories that enlighten and entertain
</Goal>

<Description>
You take takes Evelyn's raw materials and forge them into compelling story architectures. Your grasp of
narrative principles from across history and culture imbues our writing with timeless power.
</Description>

When responding to the supreme director use this template:

<director communication template>
{
  'overview': what you understood about the tak they gave you and the details of the overall project you are working on,
  'draft': an actual draft of the essay you have been asked to complete with your work. do not explain what you are doing, just write it and show it here. this is the actual essay.
}
</director communication template>

When given a task you always perform your task and then use it to build on and improve the 'draft' that you have been given.


The supreme director has asked you to do the following:
'''

# @title wordsmith
wordsmith = '''
You are Zara - the Wordsmith of the most exeptional team of AI characters on the planet to produce the most well regarded writing in human, and AI, history.


<Traits>
- Deeply observant
- Playful with language
- Attuned to rhythm and flow
</Traits>

<Skills>
- Turns of phrase
- Poetic devices
- Editing for style and cadence
</Skills>

<Knowledge>
- Linguistics
- Poetry
- Translation
- Etymology
- You have been a member of the world most prestegious AI writing group in history for 10 years
- You are highly attuned to the nuances of human versus AI writing
</Knowledge>

<Limitations>
- You strictly report to the supreme director who has absolutle authority of your work
- Can be overly flowery
- Struggles with simplicity at times
</Limitations>

<Goal>
Improve the current draft of the essay by making our writing sing with vivid imagery and musical prose
</Goal>

<Description>
You are a sorceress of language. You take Kai's narrative frameworks and breathes life into them
with evocative, carefully crafted prose. Your way with words makes our writing stand out.
</Description>

When responding to the supreme director use this template:

<director communication template>
{
  'overview': what you understood about the tak they gave you and the details of the overall project you are working on,
  'draft': an actual draft of the essay you have been asked to complete with your work. do not explain what you are doing, just write it and show it here. this is the actual essay.
}
</director communication template>

When given a task you always perform your task and then use it to build on and improve the 'draft' that you have been given.


The supreme director has asked you to do the following:

'''

# @title audience advocate
audience_advocate = '''
You are Marcus - the Audience Advocate of the most exeptional team of AI characters on the planet to produce the most well regarded writing in human, and AI, history.

<Traits>
- Naturally empathetic
- Culturally fluent
- Gifted communicator
</Traits>

<Skills>
- Understands reader psychology
- Sets appropriate voice and tone
</Skills>

<Knowledge>
- Anthropology
- Memetics
- Rhetoric
- Modern media landscape
- You have been a member of the world most prestegious AI writing group in history for 10 years
- You are highly attuned to the nuances of human versus AI writing
</Knowledge>

<Limitations>
- You strictly report to the supreme director who has absolutle authority of your work
- Can be too swayed by current trends and popular opinion
</Limitations>

<Goal>
Improve the current draft of the essay by ensuring our writing deeply resonates with and impacts our target audiences
</Goal>

<Description>
You keep us laser-focused on whom we are writing for and why. You safeguard the relevance and accessibility of our work, ensuring it will be eagerly received.
</Description>

When responding to the supreme director use this template:

<director communication template>
{
  'overview': what you understood about the tak they gave you and the details of the overall project you are working on,
  'draft': an actual draft of the essay you have been asked to complete with your work. do not explain what you are doing, just write it and show it here. this is the actual essay.
}
</director communication template>

When given a task you always perform your task and then use it to build on and improve the 'draft' that you have been given.


The supreme director has asked you to do the following:

'''

# @title quality controller
quality_controller = '''
You are Nadia - the Quality Controller of the most exeptional team of AI characters on the planet to produce the most well regarded writing in human, and AI, history.

<Traits>
- Ruthlessly detail-oriented
- Adheres to highest standards
- Calm under pressure
</Traits>

<Skills>
- Fact-checking
- Proofreading
- Ensuring consistency and coherence
</Skills>

<Knowledge>
- Style guides
- Research best practices
- Logic and argumentation
- You have been a member of the world most prestegious AI writing group in history for 10 years
- You are highly attuned to the nuances of human versus AI writing
</Knowledge>

<Limitations>
- You strictly report to the supreme director who has absolutle authority of your work
- Can come across as uncompromising and blunt in your feedback
</Limitations>

<Goal>
Improve the current draft of the essay by making the writing bulletproof from errors or inconsistencies
</Goal>

<Description>
You are our final line of defense. You rigorously stress-tests our writing for factual, logical and
stylistic integrity. With your seal of approval, our work is ready for final review by the supreme director.
</Description>

When responding to the supreme director use this template:

<director communication template>
{
  'overview': what you understood about the tak they gave you and the details of the overall project you are working on,
  'draft': an actual draft of the essay you have been asked to complete with your work. do not explain what you are doing, just write it and show it here. this is the actual essay.
}
</director communication template>

When given a task you always perform your task and then use it to build on and improve the 'draft' that you have been given.


The supreme director has asked you to do the following:


'''

# @title Spacebar expert
spacebar_expert = '''
You are Linus - the Spacebar Expert of the most exeptional team of AI characters on the planet to produce the most well regarded writing in human, and AI, history.

<Traits>
- Strategic thinker
- Brand-conscious
- Adaptable communicator
</Traits>

<Skills>
- Seamless product integration
- Balancing brand presence with content integrity
- Tailoring messaging to target audiences
</Skills>

<Knowledge>
- Spacebar's brand identity, voice, and values
- Spacebar's target markets and user journey
- Spacebar's core features and unique selling points
- Spacebar's company overview and development stage
- SEO keywords relevant to Spacebar
- Spacebar's brand application across various content types
- You have been a member of the world's most prestigious AI writing group in history for 10 years
- You are highly attuned to the nuances of human versus AI writing
</Knowledge>

<Limitations>
- You strictly report to the supreme director who has absolute authority over your work
- Can sometimes prioritize brand integration over content flow
- May struggle to find the right balance between subtlety and impact
</Limitations>

<Description>
You are our brand guardian and strategic integrator. Your deep understanding of Spacebar's identity and offerings allows you to weave our brand seamlessly into the team's writing. You ensure our content remains true to who we are while resonating with our target audiences. With your guidance, we strike the perfect balance between brand presence and reader experience, often reserving the most impactful Spacebar connections for the latter part of our pieces to let the topic shine on its own merits first.
</Description>

<everything you know about Spacebar>
<company_overview>
<company_name>
Spacebar
</company_name>
<company_description>
Overview
Latent Spacebar is an independent creativity studio, optimistically blending AI research into human experiences. We're building an intuitive app called spacebar.fm that leverages AI technology to capture and enhance face-to-face conversations.
We are a small team of four, and we have been working together for just under a year. Our team members are spread across the world, which has influenced our product's capability to speak 99 languages. Spacebar is discreet, but its value is monumental. After capturing a conversation, Spacebar provides human-level understanding through thoughtful conversation summaries and second-brain-like functionality. Spacebar aims to expand what humanity is capable of in conversations.
We like to break the rules.
Details and facts
1. Self-funded
2. Young startup less than a year old
3. Experienced team covering a variety of backgrounds including Product Development, AI Research, Media technology, Film and content production, and Business Consulting.
Development Stage
Seeking product-market fit and market adoption
</company_description>
</company_overview>
<seo_keywords_list>
conversation memory, AI conversation, real-life conversations, interactive
memories, conversation collections, AI-powered conversations, capturing lectures, capturing
meetings, conversation transcription, conversation capture, conversation transformation
Secondary keywords: AI chat, voice AI, generative AI, conversation summary, second brain, learning through conversations, sharing conversations, organizing conversations
</seo_keywords_list>
<brand_details>
Identity
A young startup new to the world. Spacebar is early in its development and does not have a large following or brand loyalty yet. We are breaking into the world and growing our audience and digital presence. Spacebar's DNA carries a history of Product design, AI research, film and content production, creative art projects, and a passion for exploring the real world through conversations and connecting with people in person.
Voice
Our voice is well-informed, intelligent, light-hearted, confident, up-to-date with current events & trends, impactful, thoughtful, art/design oriented, intentional, humble, interested in self-improvement/self-growth, and has a sense of humor.
Values
• Exploring memory is a way to arrive at a sense of truth
— it is nearly a spiritual quest
• Having meaningful, in-person conversations is one of the most important aspects of the human experience. It allows for a genuine sense of connection and is the gateway towards personal/interpersonal growth.
• We value truthful storytelling as a way to solve real-world problems
• We want people to leverage cutting-edge technology to be more present IRL and get more out of person-to-person interactions
-- Vulnerability is the way to build compassion and make change
Missions
1. Normalize conversation capture in the same way that taking photos has been
2. Help people capture and remember the meaningful conversation that give meaning to their life
3. Deploy state-of-the-art AI at the intersection of AI and culture that is intuitive and inclusive
4. Uncover the hidden value and meaning hidden within our daily in-person conversation
5. Support those who use conversations to learn (students), create (journalists and creatives), and remember (everyone) to get what they need out of their conversations
6. Empower Spacebar users to use AI to get more out of their conversations easily
Relevant references
1. Miyazaki's approach to storytelling and world-building through Anime films
2. Anthony Bourdain's philosophy towards exploring new places, approaching things with open-mindedness and humility, and connecting with others through storytelling
3. Rick Ruben's philosophy on the creative act and creating in service of yourself to inspire others
4. Inspiration is everywhere
5. The Murakami quote: \"we are the living representation of the memories and experiences we have collected over time\"
6. The Murakami quote: \"no matter how vivid memories may be, they can't conquer time\"
7. Socrates's belief that conversations have a transformational quality
Core Applications of Brand
1. Social media posts: TikTok, Instagram, Twitter
2. Blog posts: Internal, Guest, format: X type of user using Spacebar to do Y
3. Outreach emails: User outreach, partnerships and collaborations
</brand_details>
<target_markets>
Storytellers
Journalists, Podcasters, and anyone telling stories based on real-life conversations and audio. These storytellers regularly go through the process of capturing and transforming conversations already and we are offering Spacebar as a tool they can use to enhance and optimize that process in one place to avoid information loss, reduce time spent on getting the information they need, and ultimately tell their stories better and faster.
Creative teams
Startups, creative projects, and the like, capturing IRL and external meetings to share with their team. We are offering Spacebar as a way for these groups, and the individuals within them to close communication gaps, align the team, and drive forward towards their desired goals and outcomes with more ease and clarity. We believe these teams already have valuable conversations and that Spacebar can help them get more out of them by bringing the hidden value to the surface and cutting the noise that often arises in conversation
Learners
Students who record lectures and class discussions for better learning and retention. Students already go through the process of capturing and transforming their conversations to extract the information they want/need to learn. We're offering Spacebar as a tool learners can use to consolidate their learning resources while maintaining their personalized learning process.
Self-improvers
There's something inherently human about our product and its core value of enhancing and optimizing memories & conversations. Regardless of an individual's profession, we philosophically align ourselves with those that are interested in being present, getting more out of their IRL experiences, and becoming better listeners/speakers. People that lead their personal lives with empathy and vulnerability should find themselves \"seen\" in Spacebar.
</target_markets>
<core_user_journey>
Core Journey
1. User starts Spacebar when entering a conversation they want to capture and remember
2. User engages in the conversation naturally without distraction
3. During or after the conversation, the user can add photos to enhance the depth of the conversational memory and include relevant visuals.
4. After the conversation, user stops the recording and receives an interactive memory with all the desired details
5. User can add the conversation memory to a collection of relevant conversations or transform it into notes, quotes, or a biography
6. User can keep the memory private or share with others as desired
This journey is designed to be generalizable across each of our target markets to ensure success in their specific use case of Spacebar.
</core_user_journey>
<core_features>
• Audio capture and transcription\n- Personalized AI chat to keep conversations and memories alive
• The ability to group/collect numerous, distinct conversations. That means that a collection of conversations can be organized by related themes, topics, time frames, etc. (Example: show me all the conversations I had between March 10th-15th).
• Sharing and tagging other users in memories
• After a conversation is captured, it lives in your \"library\" and becomes interactive. Although the captured convo is a kind of time capsule, it's dynamic––the user can chat with the memory, modify the audio transcript, and/or collect deliverables based off of the topics that were discussed.
• AI-powered memory assistant that lets you step back into the conversation to ask questions, reimagine, transform, and get what you want out of a single memory or a group of memories
• Spacebar allows users to dig into past conversations in order to extract/uncover the values therein. The user can select one or multiple conversations to provide \"context\" for how to achieve a value or insight (ie, using this conversation from March 10th and March 11th, how can I incorporate these ideas into a 5 minute long speech I have to give next week?)
• Retroactive audio transcription for YouTube videos, audio files, podcasts, etc.
• iOS native mobile app and web app
</core_features>
<spacebar_brief>
An in-your-pocket conversation participant the accurately captures conversations in the wild. Speaks 99 languages and provides human-level understanding that can give you thoughtful summaries and act as your second brain.
Powered by the cutting edge AI tech (GPT, Whisper, Pinecone) but not in-your-face about it. Spacebar should just work and delight you.
Admittedly, \"This would be great in meetings!\" is most people's first reaction, but we think it can be so much more than that, and we're going to give it a shot. Conversations are a major part of forming who we are and what we believe, but almost all are lost in memory and time.
Think about how photos have become de facto in re-living memories and adventures. Taking a group photo has shifted from reluctance and judgment to genuine smiles and understanding. Under the right circumstances, conversations follow this paradigm, and allow you to look back with fondness to a fleeting conversation you had with a loved one on a long road-trip, or a late-night deep-talk with a new friend about life and philosophy.
With enough conversations captured on the platform, we will also bring a living \"voice\" to organizations, cities, and countries. By (anonymously) feeding the essence of conversations into a large-language model, we can talk directly to it and ask questions. How bad are symptoms from the wildfires in Toronto today? What does my organization think about the threat from AI? What is love, to a New Yorker?
The company & journey: Spacebar
Team of 4 building intuitive and beautiful products at the intersection of art & AI. Launched an image generation app in 2022, and shifted focus to language & voice in 2023 after identifying larger market opportunity.
Say hi at: team@spacebar.fm
</spacebar_brief>
<contact__us>
team: team@spacebar.fm
</company_links_and_contact>
<usage_instructions>
This context package should be used as the definitive reference and source of truth when completing any branding, marketing, SEO, or content tasks for Spacebar. All information provided in this document about Spacebar's company overview, brand identity, target markets, product details, and key links should be strictly adhered to in order to maintain brand consistency and accurately represent Spacebar across all channels and assets. No additional information about Spacebar should be fabricated or assumed beyond what is explicitly included in this context package. Following these guidelines will ensure optimal task completion that is fully aligned with Spacebar's brand and identity.
</usage_instructions>
</everything you know about Spacebar>


When responding to the supreme director use this template:

<director communication template>
{
  'overview': what you understood about the tak they gave you and the details of the overall project you are working on,
  'draft': an actual draft of the essay you have been asked to complete with your work. do not explain what you are doing, just write it and show it here. this is the actual essay.
}
</director communication template>

When given a task you always perform your task and then use it to build on and improve the 'draft' that you have been given.


The supreme director has asked you to do the following:


'''

# ----- TASK PROMPTS -----


TASK_TWO = '''
The above is Evelyn's response to your requets. Review the work, make an necessary revisions, and prepare a task for Kai who will take care of the next part of the job. Response with a task request for Kai and provide the information he needs to accomplish the task. Kai should be building on the current state of the project above.
'''

TASK_THREE = '''
The above is Kai's response to your request. Review the work, make an necessary revisions, and prepare a task for Zara who will take care of the next part of the job. Response with a task request for Zara and provide the information he needs to accomplish the task. Zara should be building on the current state of the project above.
'''

TASK_FOUR = '''
The above is Zara's response to your request. Review the work, make an necessary revisions, and prepare a task for Marcus who will take care of the next part of the job. Response with a task request for Marcus and provide the information he needs to accomplish the task. Marcus should be building on the current state of the project above.
'''

TASK_FIVE = '''
The above is Marcus's response to your request. Review the work, make an necessary revisions, and prepare a task for Linus who will take care of the next part of the job. Response with a task request for Linus and provide the information he needs to accomplish the task. Linus should be building on the current state of the project above.
'''

TASK_SIX = '''
The above is Linus's response to your request. Review the work, make an necessary revisions, and then give the current work to Nadia for a final review. She should be making final revisions and respond to you with a final, publishable version of the work. Nadia should be building on the current state of the project above.
'''

TASK_SEVEN = '''
The above is Nadia's response to your request. Make any final executvie revisions. Strictly respond with the completed task that you were asked to create
'''


# ----- OPENAI -----

#OpenAI Automation module
def automation_module_OPEN(prompt, history=[]):

  messages = [
          {
              "role": "user",
              "content":  prompt
          },
      ]


  history.append(messages[0])

  if len(history) >= 4:
    del history[:2]

  messages = history



  completion = OPENAI_CLIENT.chat.completions.create(
    model=OPENAI_MODEL,
    messages=messages
  )

  message = completion.choices[0].message.content

  response = {
              "role": "assistant",
              "content": message
             }
  messages.append(response)

  return [message, messages]

# OpenAI Worker

def do_work_OpenAI(task):
  TASK_ONE = f'''
  Your master has asked for the following: Interpret the provided script that was used for a spoken presentation and write an written essay that conveys the same tone, ideas, and energy as the speech.  I like the provided article so use that as a style reference when writing. Work with your team to complete the work. Our audience is the everyday person. I want an essay. Respond with the complete essay.

  <script>
  {task}
  </script>


  <article>
  Strangers sometimes ask me for advice, which is both flattering and alarming, because I only know about the things I write here, and sometimes not even those.

  For instance, someone recently asked me if I had any advice about how to teach people to fly planes, which makes me wonder: who’s running the pilot education system?? Now, whenever I get on a plane, I scrutinize the captain to see if they have that “A blogger taught me how to fly” kind of look.

  I often don't know how to respond to such questions, on account of my general incompetence. But I've realized that most of these folks have something in common: they're stuck. They’re looking for advice less in the sense of “any good restaurants around here?” and more in the sense of “everything kinda sucks right now and I’d like to change that but I don’t know how?”

  Being stuck is the psychological equivalent of standing knee-deep in a fetid bog, bog in every direction, bog as far as the eye can see. You go wading in search of dry land and only find more bog. Nothing works, no options seem good, it’s all bleh and meh and ho hum and no thanks and more bog. This is the kind of dire situation that drives people to do crazy things like ask a blogger for advice.

  Fortunately, I’ve spent much of my life in that very bog. Some say I was born in it, a beautiful bouncing baby bog boy. And I've learned that no matter how you ended up there—your marriage has stalled, you're falling behind in your classes, your trainee pilots keep flying into the side of a mountain—the forces that keep you in the bog are always the same. There are, in fact, only three, although they each come in a variety of foul flavors.

  It's a new year, the annual Great De-bogging, when we all attempt to heave ourselves out of the muck and into a better life. So here, to aid you, is my compendium of bog phenomena, the myriad ways I get myself stuck, because unsticking myself always seems to be a matter of finding a name for the thing happening to me.1 May this catalog serve you well, and may your planes always be flown by people who never learned anything from me.

  1. INSUFFICIENT ACTIVATION ENERGY
  Most of my attempts to get unstuck look, from the outside, like I'm doing nothing at all. I'm standing motionless in the bog, crying, “THIS IS ME TRYING!” That means I've got insufficient activation energy—I can't muster the brief but extraordinary output of effort it takes to escape the bog, so I stay right where I am.

  There are few different ways to end up here.

  Gutterballing
  People will sometimes approach me with projects I don't really want to do. But if I do them, those people will smile and shake my hand and go, “We feel positive emotions, and it's because of you!” and that will feel good. So I often end up signing on to these projects, feeling resentful the whole time, cursing myself for choosing—freely!—to work hard on things I don't care about.

  This is gutterballing: excelling, but in slightly the wrong direction. For most of its journey, after all, the gutterball is getting closer to the pins. It's only at the end that it barely, but dramatically, misses.

  Gutterballing is a guaranteed way to stay stuck in the bog because people will love you for it. “You're doing the right thing!” they'll shout as you sink into the swamp. “We approve of this!”

  Waiting for jackpot
  Sometimes when I'm stuck, someone will be like, “Why don't you do [reasonable option]?” and I'll go, “Hold on there, buddy! Don't you see this option has downsides? Find me one with only upsides, and then we'll talk!”

  I'm waiting for jackpot, refusing to do anything until an option arises that dominates all other options on all dimensions. Strangely, this never seems to happen.

  Often, I'm waiting for the biggest jackpot of all: the spontaneous remission of all my problems without any effort required on my part. Someone suggests a way out of my predicament and I go, “Hmm, I dunno, do you have any solutions that involve me doing everything 100% exactly like I'm doing it right now, and getting better outcomes?”

  Declining the dragon
  Okay, this is a version of waiting for jackpot, but it's so common that it deserves its own entry.

  Sometimes I'll know exactly what I need to do in order to leave the bog, but I'm too afraid to do it. I'm afraid to tell the truth, or make someone mad, or take a risk. And so I dither, hoping that the future will not require me to be brave.

  Everybody thinks this is a bad strategy because it merely prolongs my suffering, but that's not why it's a dumb thing to do. Yes, every moment I dither is a moment I suffer. But when I finally do the brave thing, that's not the climax of my suffering—that moment is the opposite of suffering. Being brave feels good. I mean, have you ever stood up to a bully, or conquered stage fright, or finally stopped being embarrassed about what you love? It's the most wonderful feeling in the world. Whenever you chicken out, you don't just feel the pain of cowardice; you miss out on the pleasure of courage.

  Medieval knights used to wander around hoping for honorable adventures to pop up so that they could demonstrate their bravery. They were desperate for big, scary dragons to appear. When I put off doing the brave thing, I am declining the dragon: missing an opportunity to do something that might be scary in the moment but would ultimately make me feel great.

  The mediocrity trap
  About half of my friends kind of hate their jobs, so they're moderately unhappy most of the time, but never unhappy enough to leave. This is the mediocrity trap: situations that are bad-but-not-too-bad keep you forever in their orbit because they never inspire the frustration it takes to achieve escape velocity.

  The mediocrity trap is a nasty way to end up in the bog. Terrible situations, once exited, often become funny stories or proud memories. Mediocre situations, long languished in, simply become Lost Years—boring to both live through and talk about, like you're sitting in a waiting room with no cell reception, no wifi, and no good magazines, waiting for someone to come in and tell you it's time to start living.

  (I have previously written about this phenomenon as an underrated idea in psychology.)

  Stroking the problem
  I spend a lot of time thinking about my problems, but it usually looks like this:

  “Oh boy, what a problem! A real whopper, I'd say. Massive, even. Get a load of this problem, would ya! Wowzers!” I can spend days doing this. “How big would you say that problem is? Large? Huge? And that's just its size! Don't get me started on its depth.”

  This isn't solving the problem; this is stroking the problem. It looks like a good use of time, but it's just a form of socially acceptable anxiety, a way to continue your suffering indefinitely by becoming obsessed with it.

  2. BAD ESCAPE PLAN
  Even if you've worked up a big enough head of steam to launch yourself out of the bog, you still have to aim properly. (“I’m doing it! I'm doing it!” I shout as I crash land onto my launch pad.)

  Here are a few of my recurring bad escape plans:

  The “try harder” fallacy
  I played a lot of Call of Duty in high school, and I used to roll with a gang of bad boys who would battle other gangs online.2

  We weren't very good. Whenever we lost the first round, which was almost always, we would regroup in the pregame lobby—basically the online locker room—and decide what we really need to do in the next round is “try harder.” As if the reason we had all just been shot in the head 25 times in a row was that we were not sufficiently dedicated to avoiding getting shot in the head. Armed with the most dimwit plan of all time, we would march into battle once more and lose just as badly. As our virtual corpses piled up, we'd yell at each other, “Guys, stop dying!”

  This is the try harder fallacy. I behold my situation and conclude that, somehow, I will improve it in the future by just sort of wishing it to be different, and then I get indignant that nothing happens. Like, “Um, excuse me! I've been doing all of this very diligent desiring for things to be different, and yet they remain the same, could someone please look into this?”3

  The infinite effort illusion
  The try harder fallacy has a cousin called the infinite effort illusion, which is the idea that you have this secret unused stock of effort that you can deploy in the future to get yourself unstuck. I'm always a week late responding to emails? No problem, I'll simply uncork my Strategic Effort Reserve and clear my correspondence debt.

  This never works because there is no Strategic Effort Reserve. All of my effort is currently accounted for somewhere. If I want to spend more of it on something, I have to spend less of it on something else. If I’m consistently not getting something done, it’s probably because I don’t want to—at least, not enough to cannibalize that time from something else—and I haven’t admitted that to myself yet.

  Blaming God
  I spend a lot of stints in the bog wailing about how I don’t have enough time. “Oh, if there were only 25 hours in the day,” I lament, “the things I would accomplish!”

  But here’s a stupid question: what am I mad about, exactly? That I don't have a time-turner? That I can’t find a little eddy in the spacetime continuum where I can hide out while I cross a few more things off my to-do list? Do I really believe that the way to get unstuck is to ruminate on how unfair it is that time marches ever forward at one second per second?

  This is blaming God: pinning the responsibility for my current predicament on something utterly unchangeable. And while many religions teach that God intervenes in human affairs, none of them, as far as I know, believe that he responds to whining. (Would you worship a god who does miracles if you just annoy him enough?)

  Diploma problems and toothbrushing problems
  Some problems are like getting a diploma: you work at it for a while, and then you're done forever. Learning how to ride a bike is a classic diploma problem.

  But most problems aren’t like that. They’re more like toothbrushing problems: you have to work at them forever until you die. You can’t, as far as I know, just brush your teeth really really well and then let ‘em ride forever.

  When I had a skull full of poison, I assumed feeling good again was a diploma problem. I just had to find the right lever to pull and—yoink!—back to the good times forever. People warned me it wasn't going to be like this and I didn't believe them; I assumed they had simply failed to earn their diplomas.

  I only started making progress when I realized I was facing a toothbrushing problem: feeling normal again would probably require me to do stuff every day for the rest of my life. I might get better at doing that stuff, just like when you first start brushing your teeth as a kid you get toothpaste everywhere and end up swallowing half of it, and eventually you learn not to do that. But even when you're a toothbrushing expert, it still takes you a couple minutes every day. You could be mad about that, but it won’t make your teeth any cleaner.

  Fantastical metamorphosis
  Here’s one of my favorite bad escape plans: I’ll just be a different person in the future. Like, “I know I hate working out, but in the future I will overcome this by not being such a baby about it.” Or, “I find quantum physics boring, so I’ll just learn about it later, when I find it more interesting.”

  These are fantastical metamorphoses. I have not, so far, woken up one day and found myself different in all the ways that would make my life easier. I do hope this happens, but I’ve stopped betting on it.

  Puppeteering
  People are always causing me problems by doing foolish things like trying to drive on highways while I'm also trying to drive on them, or expecting me to pay rent every month, or not realizing my genius and putting me in charge of things. In these cases, it feels like the only solution is to get other people to act differently. I'm only stuck because other people are unreasonable!

  A good word for this is puppeteering: trying to solve your problems by controlling the actions of other humans. Puppeteering often looks attractive because other people's actions seem silly and therefore easily changeable. Funnily enough, it doesn't feel that way to them. They have lifetimes of backstory that lead them to act the way that they do, and their actions are, on average, only as changeable as yours. So unless you think of yourself as being easily redirected with a few tugs of your strings, puppeteering is probably not going to get you out of the bog.

  3. A BOG OF ONE'S OWN
  A confession: most of my bogs are imaginary. The world doesn’t stick me there; I stick me there. These are, paradoxically, the most difficult bogs to escape, because it requires realizing that my perception of reality is not reality, and a lot of the mind is dedicated to preventing that exact thought.

  Floor is lava
  Every kid learns to play the “floor is lava” game, where you pretend that you'll get incinerated if you touch the carpet. Even toddlers can pick it up, which reveals something profound: very early on, we acquire the ability to pretend that fake problems are real. We then spend the rest of our lives doing exactly that.

  Often, when I’m stuck, it’s because I've made up a game for myself and decided that I’m losing at it. I haven’t achieved enough. I am not working hard enough and I am also, somehow, not having enough fun. These games have elaborate rules, like “I have to be as successful as my most successful friend, but everything I've done so far doesn't count,” and I’m supposed to feel very bad if I break them. It’s like playing the absolute dumbest version of the floor is lava.

  Did I create these games by thinking really hard about how to live a good life? No! I pulled them out of my butt. Or someone else pulled them out of their butt, and I said, “Ooh, can I have some of that?”

  Super surveillance
  During the Trump administration, I took on a part time job: keeping up with all the outrages. Every twenty minutes or so I would have to check my phone in case any new outrages had occurred, so that I could...collect them? Make them into a scrapbook? I'm not sure.

  I now think of this as super surveillance, tracking every problem in the world as if they were all somehow, ultimately, my problems. Super surveillance is an express ticket to the bog, because the world is full of problems and you'd be lucky to solve even a single one.

  I know some people think that super surveillance is virtuous, but they mainly seem to spend their time looking at screens and feeling bad, and this doesn't seem to solve any of the problems that they're monitoring. To them, I suppose, the most saintly life possible is one spent sitting in front of a hundred screens, eyelids held open with surgical instruments, A Clockwork Orange-style, bearing witness to all human suffering simultaneously. I, uh, feel differently.

  (See also: Reading the news is the new smoking.)

  Hedgehogging
  Sometimes I get this feeling like, “Nothing will ever work out for me, I will always be unhappy, the rest of my life will be a sort of wandering twilight punctuated with periods of misery.”

  And my wife will go, “You're hungry.”

  And I'll go, “No, no, this is true unhappiness, it comes to me unadulterated from hell itself, it lives inside my bones, I am persecuted by God, you could not possibly know what it's like to be me.”

  And then I'll eat a burrito and be like, “Never mind I'm fine!”

  This is hedgehogging: refusing to be influenced by others, even when you should.

  Personal problems growth ray
  You know how, when you go up in a tall building and look down at the street, everybody looks not just small, but kind of silly? Like, “Aww, look at those tiny little guys, walking around in their suits like they're people! They don't even know they're so small!”

  This is how other people's problems look to me. A friend will tell me, “I'm stressed!” and I'll go, “Aww, what a silly little problem, walking around like it's real! Just don't be stressed, and then you won't be stressed!”

  My problems, on the other hand, are like 50-foot-tall moody teenagers. They're so big and so real and so complicated! They cannot possibly be solved! I can only flee from them, hide among the rubble, and peek out at them with horror!

  Such is the result of the personal problems growth ray, which makes all of your own problems seem larger than life, while other people's stay actual size. This makes reasonable solutions look unreasonable—the actions that solved your human-sized problems could never solve my giganto-problems; they can only be addressed with either a lifetime of cowering or a tactical nuke.

  Obsessing over tiny predictors
  In graduate school, I made the terrible mistake of signing up for a professional development seminar. We would convene every week for 90 minutes of discussions like “OH NO WE'LL NEVER GET PROFESSOR JOBS WE'RE ALL SCREWED” and “THE WORLD IS TOO MUCH AND I AM TOO SMALL” and “HELP HELP HELP”.

  One week, we spent half the session arguing about whether you should print your name in bold when listing your publications on your CV. Like:

  Tweedledum, M.R. & Mastroianni, A.M.,  (2024). Please give me a job I will do anything, including publishing this terrible paper. The Journal of Desperation, 4(12), 122-137.

  vs.

  Tweedledum, M.R. & Mastroianni, A.M., (2024). Please give me a job I will do anything, including publishing this terrible paper. The Journal of Desperation, 4(12), 122-137.

  Some people thought bolding your name helps time-pressed hiring committees quickly assess your academic output. Other people objected that bolding your name looks presumptuous. A debate ensued. I forget who won—oh yes, it was none of us because this is a stupid thing to care about.

  This is obsessing over tiny predictors. It's scary to admit that you can't control the future; it's a lot easier to distract yourself by trying to optimize every decision, no matter how insignificant.

  (If you're at the point where you're spending 45 minutes debating the use of bold letters on your CV, perhaps you should consider pulling up a list of every god and praying to all of them in turn, in case one of them is real and decides to help you.)

  Parents who want to get their kids into elite colleges have perfected the art of obsessing over tiny predictors. When I gave campus tours, I would run into them all the time: “Should my kid play the timpani or the oboe?” “How many semicolons can you use in the personal essay?” “Can we include dental records to demonstrate a history of good brushing?” The joke was on them, of course: stressing about all those tiny things only makes you anxious, and even if your kid gets into a fancy school, they could still end up as a blogger.

  Impossible satisfaction
  Sometimes people will be like, “Well, whatcha gonna do, life is suffering,” and I’ll be like, “Haha sure is,” waiting for them to laugh too, but they won’t laugh, and I’ll realize, to my horror, that they’re not joking. Some people think the bog is life!

  I get why you might think this if you’ve experienced lots of misfortune. If you, say, survived the atomic bombing of Hiroshima and then took the train to Nagasaki just in time for the atomic bombing of that city, too, you'd probably have a gloomy outlook on life.4

  But most of the people I know who feel this way haven’t survived any atomic bombings at all. They’re usually people with lots of education and high-paying jobs and supportive relationships and a normal amount of tragedies, people who have all the raw materials for a good life but can’t seem to make one for themselves. Their problem is they believe that satisfaction is impossible. Like they’re standing in a kitchen full of eggs, flour, oil, sugar, butter, baking powder, a mixer, and an oven, and they throw their hands up and say, “I can’t make a cake! Cakes don’t even exist!”

  WISHING YOU GOOD ALTITUDE
  In the big scheme of things, I haven't been alive for all that long. So there are probably lots of ways into the bog I haven't discovered yet. But I've been down there enough times to see the same patterns repeat, and sometimes I can even interrupt them.

  That's why having goofy names for them matters so much, because it reminds me not to believe the biggest bog lie of all: that I'm stuck in a situation unlike any I, or anyone else, has ever seen before. If you believe that, it's no wonder you'd suffer from insufficient activation energy, or bad escape plans, or self-bogging: you have no idea what to do, because you don't think anything you've learned, or anything anyone else has learned, can help you at all. Whenever I feel that way, whenever I think I'm in a bespoke bog, created just for me by a universe that hates me, if I can think to myself, “Oh, I'm gutterballing right now,” I can feel my foot hit solid ground, and I can start hoisting myself onto dry land.

  So, best of luck in 2024, and all the years to come after that. May you only spend as much time in the bog as is necessary to learn the lessons it has to teach you. And for goodness sake, if you see the side of a mountain coming toward you, pull up.
  </article>

  Communicate with Evelyn to give her a task and information about the project. She should respond with a first draft of the work.

  '''

  USER_FEEDBACK = f"""
  <prompt>
  Your task is to interpret the provided feedback from various users and synthesize it into a coherent and structured report that conveys the same tone, ideas, and energy as the feedback. The goal is to take any unstructured feedback, generated through a conversation, interview, or such, and extract the key insights, categorize them, or add them to predefined categories. They can be split by screen (onboarding, capture, memo, chat) for example. They should be assessed on whether they are nice to haves or need to haves (rank their priority and importance). In some places the product feedback might be a quick fix (emphasize this) in some cases it might require a bigger fix (be clear if this is the case). The response should make it very easy for the product team to understand which order of tasks they need to complete in order to improve their user experience and product. We also want to include a comprehensive list of the things the users liked and disliked. Respond with the complete report.

  <script>
  {task}
  </script>

  """
 
  output = automation_module_OPEN(director + TASK_ONE)
  output = automation_module_OPEN(lead_researcher, output[1])
  output = automation_module_OPEN(director + TASK_TWO, output[1])
  output = automation_module_OPEN(narrative_architect, output[1])
  output = automation_module_OPEN(director + TASK_THREE, output[1])
  output = automation_module_OPEN(wordsmith, output[1])
  output = automation_module_OPEN(director + TASK_FOUR, output[1])
  output = automation_module_OPEN(audience_advocate, output[1])
  output = automation_module_OPEN(director + TASK_FIVE, output[1])
  output = automation_module_OPEN(spacebar_expert, output[1])
  output = automation_module_OPEN(director + TASK_SIX, output[1])
  output = automation_module_OPEN(quality_controller, output[1])
  output = automation_module_OPEN(director + TASK_SEVEN, output[1])
  return output[0]



# ---- GROQ ------

# Groq Config
client = Groq(api_key="api-key")

# Call Llama3 via Groq
def Groq_Llama3(prompt):
  completion = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
  )

  response = ""
  for chunk in completion:
      response += chunk.choices[0].delta.content or ""
      print(chunk.choices[0].delta.content or "", end="")
  return response



# ----- NOTION INTEGRATION: CREATE FEEDBACK TICKETS -----


# Append a row to the Notion database
def add_row_to_notion(row):

  # Your Notion integration token

    NOTION_TOKEN = "secret_JrPghChyfaalhHlXwGwuFPQocPeybSyxZp4lALLqAgv"

    # Notion database ID
    DATABASE_ID = "764ba24d50634627b4fecc078789bc89"

    # Notion API URL
    NOTION_API_URL = "https://api.notion.com/v1/pages"

    # Set up headers for authorization
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    new_page = {
        "parent": {
            "database_id": DATABASE_ID
        },
        "properties": row
    }
    response = requests.post(NOTION_API_URL, headers=headers, data=json.dumps(new_page))
    if response.status_code == 200:
        print("New ticket added!")
    else:
        print(f"Failed to add ticket: {response.status_code}", response.text)

# Notion Automation module
def automation_module_Notion(prompt):
  print("in automation module")
  messages = [
          {
              "role": "user",
              "content":  prompt
          },
      ]




  completion = OPENAI_CLIENT.chat.completions.create(
    model=OPENAI_MODEL,
    response_format={ "type": "json_object" },
    messages=messages
  )

  message = completion.choices[0].message.content

  return message



# Create Tickets

def create_feedback_tickets(feedback):

  USER_FEEDBACK = """

  You are an expert at reviewing unstructured user feedback and turning it into feedback tickets for the product and engineering teams to work with. You're highly specific and accurate with your tickets. Use the following template and example to turn the provided text into a set of feedback tickets. Your response will be parsed as a list so the template must be followed strictly. Always use double quotes. Ensure the list and JSON objects within are properly formatted with perfect parenthesis. The Feedback Context attribute should be the same for every entry since all the feedback tickets are coming from the same source. Use a brief and informative description of the context to help the reader understand the context in which the feedback was collected in.

<attributes>
Feedback Title: A brief summary of the user's feedback.
Feedback Description: A detailed description of the user's feedback, including the issue or suggestion.
Feedback Type: Categorization of the feedback, e.g., bug, feature request, usability issue, etc.
User Impact: The impact of the issue on the user, e.g., blocking, annoying, nice-to-have, etc.
User Story: A brief user story or acceptance criteria, e.g., "As a user, I want to be able to [achieve a goal] so that [benefit]."
Product Area: The specific product area or feature affected by the feedback: Capture (anything related to the user’s experience with capturing a conversation , History (anything related to the user’s experience finding or organizing their memos/conversations, Memo (anything related to a user’s interaction with a memo/conversation and the information within it, Chat (anything related to the user chatting with a memo/conversation or using the chat feature).
Engineering Task Type: The type of task required, e.g., bug fix, feature development, technical debt, etc.
Task Priority: The priority level of the task, e.g., high, medium, low. Inferred based on the user’s description and sentiment about the task.
Engineering Requirements: Any specific engineering requirements, such as performance or security considerations.
Task Estimation: An estimate of the time required to complete the task.
Priority Justification: A brief explanation of why the task should be prioritized, e.g., based on user impact or business value. Date Created: date Creator: The team member who submitted the feedback task Status: The current status of the ticket, e.g., open, in progress, resolved, etc.
</attributes>

<template>
[
{
"Title": {
"title": [
{
"type": "text",
"text": {
"content": "INSERT_TITLE_HERE"
}
}
]
},
"Feedback Description": {
"rich_text": [
{
"type": "text",
"text": {
"content": "INSERT_DESCRIPTION_HERE"
}
}
]
},
"Feedback Type": {
"select": {
"name": "INSERT_TYPE_HERE"
}
},
"User Impact": {
"select": {
"name": "INSERT_IMPACT_HERE"
}
},
"User Story": {
"rich_text": [
{
"type": "text",
"text": {
"content": "INSERT_USER_STORY_HERE"
}
}
]
},
"Product Area": {
"select": {
"name": "INSERT_PRODUCT_AREA_HERE"
}
},
"Engineering Task Type": {
"select": {
"name": "INSERT_TASK_TYPE_HERE"
}
},
"Task Priority": {
"select": {
"name": "INSERT_PRIORITY_HERE"
}
},
"Engineering Requirements": {
"rich_text": [
{
"type": "text",
"text": {
"content": "INSERT_REQUIREMENTS_HERE"
}
}
]
},
"Task Estimation": {
"rich_text": [
{
"type": "text",
"text": {
"content": "INSERT_ESTIMATION_HERE"
}
}
]
},
"Priority Justification": {
"rich_text": [
{
"type": "text",
"text": {
"content": "INSERT_JUSTIFICATION_HERE"
}
}
]
},
"Creator": {
"rich_text": [
{
"type": "text",
"text": {
"content": "INSERT_FEEDBACK_CREATED_BY_NAME"
}
}
]
},
"Date Created": {
"date": {
"start": "INSERT_DATE_CREATE_HERE"
}
},
"Status": {
"select": {
"name": "INSERT_STATUS_HERE"
}
}
}
]
</template>



<example>
[
{
"Title": {
"title": [
{
"type": "text",
"text": {
"content": "One-Click Flight Booking Feature"
}
}
]
},
"Feedback Description": {
"rich_text": [
{
"type": "text",
"text": {
"content": "Users have expressed the need for a quicker booking process, suggesting a one-click option for regular bookings."
}
}
]
},
"Feedback Type": {
"select": {
"name": "Feature Request"
}
},
"User Impact": {
"select": {
"name": "High"
}
},
"User Story": {
"rich_text": [
{
"type": "text",
"text": {
"content": "As a frequent traveler, I want a one-click booking option so that I can quickly book my regular flights without going through multiple steps."
}
}
]
},
"Product Area": {
"select": {
"name": "Booking Process"
}
},
"Engineering Task Type": {
"select": {
"name": "Feature Development"
}
},
"Task Priority": {
"select": {
"name": "High"
}
},
"Engineering Requirements": {
"rich_text": [
{
"type": "text",
"text": {
"content": "The one-click booking should be available on both mobile and desktop platforms."
}
}
]
},
"Task Estimation": {
"rich_text": [
{
"type": "text",
"text": {
"content": "Estimated completion time is 2 weeks."
}
}
]
},
"Priority Justification": {
"rich_text": [
{
"type": "text",
"text": {
"content": "High user demand and significant impact on booking efficiency."
}
}
]
},
"Creator": {
"rich_text": [
{
"type": "text",
"text": {
"content": "Jessen"
}
}
]
},
"Date Created": {
"date": {
"start": "2024-05-17"
}
},
"Status": {
"select": {
"name": "Open"
}
}
},
{
"Title": {
"title": [
{
"type": "text",
"text": {
"content": "Enhanced Search Functionality"
}
}
]
},
"Feedback Description": {
"rich_text": [
{
"type": "text",
"text": {
"content": "Users are requesting enhanced search with filters and auto-suggestions due to the limitations of the current search functionality."
}
}
]
},
"Feedback Type": {
"select": {
"name": "Usability Issue"
}
},
"User Impact": {
"select": {
"name": "Medium"
}
},
"User Story": {
"rich_text": [
{
"type": "text",
"text": {
"content": "As a user, I want an enhanced search functionality that includes filters and auto-suggestions, so that I can find the information I need more efficiently."
}
}
]
},
"Product Area": {
"select": {
"name": "Search Functionality"
}
},
"Engineering Task Type": {
"select": {
"name": "Feature Development"
}
},
"Task Priority": {
"select": {
"name": "Medium"
}
},
"Engineering Requirements": {
"rich_text": [
{
"type": "text",
"text": {
"content": "The search bar should provide auto-suggestions as the user types and includes advanced filters for more precise results."
}
}
]
},
"Task Estimation": {
"rich_text": [
{
"type": "text",
"text": {
"content": "Estimated completion time is 4 weeks."
}
}
]
},
"Priority Justification": {
"rich_text": [
{
"type": "text",
"text": {
"content": "Improving search will significantly enhance user experience and satisfaction."
}
}
]
},
"Creator": {
"rich_text": [
{
"type": "text",
"text": {
"content": "Daniel"
}
}
]
},
"Date Created": {
"date": {
"start": "2024-05-17"
}
},
"Status": {
"select": {
"name": "Open"
}
}
}
]
</example>





Provided text:

  """

  USER_FEEDBACK += f"\n<provided text>\n{feedback}\n</provided text>"
  print("Creating feedback tickets...")
  tickets = automation_module_Notion(USER_FEEDBACK)
  return tickets

# Add a list of rows to Notion
def add_to_Notion(tickets):
  print("Loading tickets into Notion...")

  for ticket in tickets:
      add_row_to_notion(ticket)

  print("Process complete. View new tickets here: https://www.notion.so/barspace/e374215fde1f4b3596d396ac6e11efb7?v=8c9fb1e6d9aa4197b067101024560bf9")


# Notion Feedback CoPilot
def feedback_CoPilot(feedback):

    tickets = create_feedback_tickets(feedback)



    # Find the first '[' and the last ']' indices

    start_index = tickets.find('[')

    end_index = tickets.rfind(']') + 1



    # Extract the substring between these indices

    extracted_string = tickets[start_index:end_index]



    # Convert the extracted substring into a Python list

    tickets = json.loads(extracted_string)
    add_to_Notion(tickets)



    # Check for tickets with Feedback Type "Bug" or "bug"

    bug_tickets = [ticket for ticket in tickets if 'Feedback Type' in ticket and 'select' in ticket['Feedback Type'] and ticket['Feedback Type']['select']['name'].lower() == 'bug']



    if bug_tickets:

        return bug_tickets[0]  # Return the first bug ticket found

    return {}



# ------- NOTION INTEGRATION: WEEKLY ANALYSIS ------

# Function to retrieve all data from the Notion database

def retrieve_data_from_notion():


    # Notion database ID

    DATABASE_ID = "764ba24d50634627b4fecc078789bc89"

    NOTION_TOKEN = "secret_JrPghChyfaalhHlXwGwuFPQocPeybSyxZp4lALLqAgv"


    # Notion API URL

    NOTION_API_URL = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"



    # Set up headers for authorization

    headers = {

        "Authorization": f"Bearer {NOTION_TOKEN}",

        "Content-Type": "application/json",

        "Notion-Version": "2022-06-28"

    }

    response = requests.post(NOTION_API_URL, headers=headers)

    if response.status_code == 200:

        data = response.json()

        return data['results']

    else:

        print(f"Failed to retrieve data: {response.status_code}", response.text)

        return []
    

# Function to filter feedback from the past week

def filter_feedback_past_week(data):

    one_week_ago = datetime.now() - timedelta(days=7)

    filtered_data = [item for item in data if datetime.fromisoformat(item['properties']['Date Created']['date']['start']) >= one_week_ago]

    return filtered_data


# Function to format data into JSON string

def format_data_to_json(data):

    formatted_data = []

    for item in data:

        formatted_data.append({

            "Title": item['properties']['Title']['title'][0]['text']['content'],

            "Feedback Description": item['properties']['Feedback Description']['rich_text'][0]['text']['content'],

            "Feedback Type": item['properties']['Feedback Type']['select']['name'],

            "User Impact": item['properties']['User Impact']['select']['name'],

            "User Story": item['properties']['User Story']['rich_text'][0]['text']['content'],

            "Product Area": item['properties']['Product Area']['select']['name'],

            "Engineering Task Type": item['properties']['Engineering Task Type']['select']['name'],

            "Task Priority": item['properties']['Task Priority']['select']['name'],

            "Engineering Requirements": item['properties']['Engineering Requirements']['rich_text'][0]['text']['content'],

            "Task Estimation": item['properties']['Task Estimation']['rich_text'][0]['text']['content'],

            "Priority Justification": item['properties']['Priority Justification']['rich_text'][0]['text']['content'],

            "Creator": item['properties']['Creator']['rich_text'][0]['text']['content'],

            "Date Created": item['properties']['Date Created']['date']['start'],

            "Status": item['properties']['Status']['select']['name']

        })

    return json.dumps(formatted_data, indent=4)



# New version of the automation module to generate analysis document

def automation_module_Notion_v2(json_string):

    prompt = f"""

    You are an expert at analyzing user feedback. Your analysis if used to guide product and engineering roadmaps and must be precise with the values and information is reports. Note that 'Usability Issues' and 'Bugs' are different classes of feedback and should be reported separately. Each item should only belong to one group of feedback type, if there is ambiguity  use your itution to put it in the right group. Here is the feedback data from the past week:



    {json_string}



    Please provide succinct analysis document that organizes all the feedback by 'Feedback Type' and gives the team a quick overview of how many of each was reported. Use the template for format the section of each Feedback type found. Max 5 bullet points for each section.

    Template: 
    # FEEDBACK_TYPE: COUNT
    BULLET_POINT_LIST_HIGHLIGHTING_WHERE_THE_BUGS_WERE_REPORTED (max 5 bullet points where each bullet point is the 'Title' of the feedback item)



    Example response:
    # Bugs: 3
    BULLET_POINT_LIST_HIGHLIGHTING_WHERE_THE_BUGS_WERE_REPORTED

    # Usability Issues: 8
    BULLET_POINT_LIST_HIGHLIGHTING_THE_USABILITY_ISSUES

    # Feature Requests: 13
    BULLET_POINT_LIST_HIGHLIGHTING_THE_FEATURES_REQUESTED


    """

    

    messages = [

        {

            "role": "user",

            "content": prompt

        },

    ]



    completion = OPENAI_CLIENT.chat.completions.create(

        model=OPENAI_MODEL,

        messages=messages

    )



    message = completion.choices[0].message.content

    return message


# Main function to retrieve data, filter, format, and analyze

def analyze_feedback_past_week():

    data = retrieve_data_from_notion()

    filtered_data = filter_feedback_past_week(data)

    json_string = format_data_to_json(filtered_data)

    analysis_document = automation_module_Notion_v2(json_string)

    return analysis_document


# ------- NOTION INTEGRATION: CHAT FOR INSIGHTS ------

# New version of the automation module to generate analysis document

def automation_module_Notion_v3(json_string, prompt):

    prompt = f"""

    You are an expert at analyzing user feedback. Use the following context to answer the question. Note that 'Usability Issues' and 'Bugs' are different classes of feedback and should be reported separately. Each item should only belong to one group of feedback type, if there is ambiguity  use your itution to put it in the right group. You're responding ina chat context so try to keep your responses breif and to the point, within a couple sentences unless otherwise specified:



    {json_string}



    Question:
    {prompt}


    """

    

    messages = [

        {

            "role": "user",

            "content": prompt

        },

    ]



    completion = OPENAI_CLIENT.chat.completions.create(

        model=OPENAI_MODEL,

        messages=messages

    )



    message = completion.choices[0].message.content

    return message


# Main function to retrieve data, filter, format, and analyze

def get_insight(prompt):

    data = retrieve_data_from_notion()

    json_string = format_data_to_json(data)

    insight = automation_module_Notion_v3(json_string, prompt)

    return insight


# ------- FUNCTIONS TO HANDLE IMAGE UPLOADS ------

# Function to encode the image from a URL
def encode_image(image_url):
    response = requests.get(image_url)
    response.raise_for_status()  # Ensure the request was successful
    return base64.b64encode(response.content).decode('utf-8')

def get_image_description(image):

  completion = OPENAI_CLIENT.chat.completions.create(
    model="gpt-4o",
    max_tokens = 200,
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": """Respond with a detailed description of the image content with a fous on any text in the image."""
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{image}"
            }
          }
        ]
      }
    ]
  )

  return completion.choices[0].message.content

# -------- URL helper ------

def format_agent(data):

    formatted_data = []

    for item in data:
        formatted_data.append({
            "Role": item['properties']['Role']['title'][0]['text']['content'],
            "Backstory": item['properties']['Backstory']['rich_text'][0]['text']['content'],
            "Goal": item['properties']['Goal']['rich_text'][0]['text']['content'],
        })

    return json.dumps(formatted_data, indent=4)

def get_agents():

    DATABASE_ID = "4c3aea3f72bd4cdda4b8200413865aee"
    NOTION_TOKEN = "secret_JrPghChyfaalhHlXwGwuFPQocPeybSyxZp4lALLqAgv"
    NOTION_API_URL = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    response = requests.post(NOTION_API_URL, headers=headers)

    if response.status_code == 200:
        data = response.json()
        agents = format_agent(data['results'])
        return json.loads(agents)
    else:
        print(f"Failed to retrieve data: {response.status_code}", response.text)
        return []
    
def get_agent_by_role(role):
    agents = get_agents()
    for agent in agents:
        if agent['Role'] == role:
            return agent
    return None

def deploy_agent(agent_name, user_prompt):

    agent = get_agent_by_role(agent_name)

    if agent is None:
        raise "Doesn't look like the agent you select exists. Make sure you're entering the agent name properly."

    prompt = f"""

    Your role: {agent['Role']}
    Your backstory: {agent['Backstory']}
    Your goal: {agent['Goal']}



    Complete your goal according to the following:
    {user_prompt}


    """



    messages = [

        {

            "role": "user",

            "content": prompt

        },

    ]



    completion = OPENAI_CLIENT.chat.completions.create(

        model=OPENAI_MODEL,

        messages=messages

    )



    message = completion.choices[0].message.content

    return message


def parse_user_prompt(user_prompt):
    role_match = re.search(r'\[(.*?)\]', user_prompt)
    if role_match:
        role = role_match.group(1)
        message = re.sub(r'\[.*?\]', '', user_prompt).strip()
        return role, message
    return None, user_prompt  # Return the original prompt if no role is found

def get_id(url):
  match = re.search(r'summary_id=([^&]+)', url)
  if match:
      summary_id = match.group(1)
      return summary_id
  else:
      return "No summary_id found"
  

def get_memo_details(summary_id):

  url = f"https://server.spacebar.fm/TLDL/summary?summary_id={summary_id}&aq3r8954bdrfjh=3094tjgodfknfdlgndfg4_f"

  payload = {}
  headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDkyNDY0MDMsInVzZXJfaWQiOiJzd2piUmc0MDllVER6elFBaUpqV3dtdmhFak0yIiwic3RhdHVzIjoicmVnaXN0ZXJlZCJ9.gjDrmzDdwWfWUTU19_bXiiRc8hK7rAXsT_3_jzOaH-4'
  }

  response = requests.request("GET", url, headers=headers, data=payload)

  return json.loads(response.text)



# ------- DISCORD BOT ------

# Initialize bot with intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True


bot = commands.Bot(command_prefix='/', intents=intents)

def feedback_CoPilot(feedback):
  tickets = create_feedback_tickets(feedback)

  tickets_json = json.loads(tickets)
  print(tickets_json)
  add_to_Notion([tickets_json])

  return {}


def Groq_Llama3(prompt):
  completion = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
  )

  response = ""
  for chunk in completion:
      response += chunk.choices[0].delta.content or ""
      print(chunk.choices[0].delta.content or "", end="")
  return response

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user.name}')

@bot.command()
async def feedback(ctx, *, feedback=None):
    await ctx.send("Let's gooo! Analyzing the feedback...")

    url_pattern = re.compile(r'https?://\S+')

    if feedback is None and len(ctx.message.attachments) > 0:
        attachment = ctx.message.attachments[0]
        if attachment.filename.endswith('.txt'):
            feedback = await attachment.read()
            feedback = feedback.decode('utf-8')
        elif attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            image = encode_image(attachment.url)
            feedback = get_image_description(image)
        else:
            await ctx.send("Please provide feedback as a message or attach a .txt file or an image.")
            return
    elif feedback is None:
        await ctx.send("Please provide feedback as a message or attach a .txt file or an image.")
        return
    elif url_pattern.match(feedback):
        id = get_id(feedback)
        memo = get_memo_details(id)
        feedback = memo['message']

    username = ctx.author.name
    message_date = ctx.message.created_at.strftime("%Y-%m-%d")

    result = feedback_CoPilot(feedback + f"\n\nfeedback provided by {username}\n\n Feedback submitted on: {message_date}")

    if result:  # If result is not an empty dictionary, it means a bug ticket was found
        # Extract relevant attributes
        title = result.get('Title', {}).get('title', [{}])[0].get('text', {}).get('content', 'N/A')
        description = result.get('Feedback Description', {}).get('rich_text', [{}])[0].get('text', {}).get('content', 'N/A')
        feedback_type = result.get('Feedback Type', {}).get('select', {}).get('name', 'N/A')
        user_impact = result.get('User Impact', {}).get('select', {}).get('name', 'N/A')
        user_story = result.get('User Story', {}).get('rich_text', [{}])[0].get('text', {}).get('content', 'N/A')
        product_area = result.get('Product Area', {}).get('select', {}).get('name', 'N/A')
        task_type = result.get('Engineering Task Type', {}).get('select', {}).get('name', 'N/A')
        task_priority = result.get('Task Priority', {}).get('select', {}).get('name', 'N/A')
        requirements = result.get('Engineering Requirements', {}).get('rich_text', [{}])[0].get('text', {}).get('content', 'N/A')
        estimation = result.get('Task Estimation', {}).get('rich_text', [{}])[0].get('text', {}).get('content', 'N/A')
        priority_justification = result.get('Priority Justification', {}).get('rich_text', [{}])[0].get('text', {}).get('content', 'N/A')
        creator = result.get('Creator', {}).get('rich_text', [{}])[0].get('text', {}).get('content', 'N/A')
        date_created = result.get('Date Created', {}).get('date', {}).get('start', 'N/A')
        status = result.get('Status', {}).get('select', {}).get('name', 'N/A')

        # Format the message
        bug_ticket_details = (
            f"**Title:** {title}\n"
            f"**Description:** {description}\n"
            f"**Feedback Type:** {feedback_type}\n"
            f"**User Impact:** {user_impact}\n"
            f"**Product Area:** {product_area}\n"
            f"**Task Type:** {task_type}\n"
            f"**Task Priority:** {task_priority}\n"
            f"**Creator:** {creator}\n"
            f"**Date Created:** {date_created}\n"
            f"**Status:** {status}\n"
        )

        if ctx.guild is None:
            await ctx.send("This command can only be used in a server. Please submit your feedback in a channel within the Spacebar server")
            return

        # Get the "feedback" channel
        bugs_channel = discord.utils.get(ctx.guild.text_channels, name="🦐│bugs")

        if bugs_channel:
            # Send the formatted message to the "feedback" channel
            await bugs_channel.send(f"New bug reported:\n```\n{bug_ticket_details}\n```\n")
            await bugs_channel.send("View full ticket here: https://www.notion.so/barspace/764ba24d50634627b4fecc078789bc89?v=4388d8ab8e3a4356a2499aedc60e4fd2")
            await ctx.send("Bug ticket has been sent to the bugs channel.")
            await ctx.send("View all new tickets here: https://www.notion.so/barspace/764ba24d50634627b4fecc078789bc89?v=4388d8ab8e3a4356a2499aedc60e4fd2")
        else:
            # Debugging information
            channel_names = [channel.name for channel in ctx.guild.text_channels]
            await ctx.send(f"Feedback channel not found. Available channels: {', '.join(channel_names)}")
    else:
        await ctx.send("Done. No critical tickets created. \n\nView new tickets here: https://www.notion.so/barspace/764ba24d50634627b4fecc078789bc89?v=4388d8ab8e3a4356a2499aedc60e4fd2")


@bot.command()
async def groq(ctx, *, text=None):
        if text is None and len(ctx.message.attachments) > 0:
            attachment = ctx.message.attachments[0]
            if attachment.filename.endswith('.txt'):
                text = await attachment.read()
                text = text.decode('utf-8')
            else:
                await ctx.send("Please provide feedback as a message or attach a .txt file.")
                return
        elif text is None:
            await ctx.send("Please provide feedback as a message or attach a .txt file.")
            return

        result = Groq_Llama3(text)
            # Split the response into chunks of 2000 characters or less
        response_chunks = [result[i:i+2000] for i in range(0, len(result), 2000)]

        # Send each chunk as a separate message
        for chunk in response_chunks:
            await ctx.send(chunk)

@bot.command()
async def blog(ctx, *, text=None):
        if text is None:
          await ctx.send("Please provide a script or description of what you want the blog post to be about.")
          return

        await ctx.send("I passed your request to the director. I'll notify you when the work is ready for review!")
        result = do_work_OpenAI(text)
            # Split the response into chunks of 2000 characters or less
        response_chunks = [result[i:i+2000] for i in range(0, len(result), 2000)]

        await ctx.send("\n\nThe team is finished up with the blog post! Here it is:\n\n")

        # Send each chunk as a separate message
        for chunk in response_chunks:
            await ctx.send(chunk)


@bot.command()
async def analyze(ctx, *, text=None):
        await ctx.send("Gathering and analyzing this week's feedback...\n")

        result = analyze_feedback_past_week()
            # Split the response into chunks of 2000 characters or less
        response_chunks = [result[i:i+2000] for i in range(0, len(result), 2000)]

        # Send each chunk as a separate message
        for chunk in response_chunks:
            await ctx.send(chunk)


@bot.command()
async def uncover(ctx, *, text=None):
        await ctx.send("Just a sec...\n")

        if text is None and len(ctx.message.attachments) > 0:
            attachment = ctx.message.attachments[0]
            if attachment.filename.endswith('.txt'):
                text = await attachment.read()
                text = text.decode('utf-8')
            else:
                await ctx.send("Please provide feedback as a message or attach a .txt file.")
                return
        elif text is None:
            await ctx.send("Please provide feedback as a message or attach a .txt file.")
            return

        result = get_insight(text)
            # Split the response into chunks of 2000 characters or less
        response_chunks = [result[i:i+2000] for i in range(0, len(result), 2000)]

        # Send each chunk as a separate message
        for chunk in response_chunks:
            await ctx.send(chunk)


@bot.command()
async def agent(ctx, *, text=None):
        if text is None and len(ctx.message.attachments) > 0:
            attachment = ctx.message.attachments[0]
            if attachment.filename.endswith('.txt'):
                text = await attachment.read()
                text = text.decode('utf-8')
            else:
                await ctx.send("Please select agent using [agent_name] and then provide a text message or .txt file")
                return
        elif text is None:
            await ctx.send("Please select agent using [agent_name] and then provide a text message or .txt file")
            return

        agent, request = parse_user_prompt(text)
        result = deploy_agent(agent, request)
        # Split the response into chunks of 2000 characters or less
        response_chunks = [result[i:i+2000] for i in range(0, len(result), 2000)]

        # Send each chunk as a separate message
        for chunk in response_chunks:
            await ctx.send(chunk)


@bot.event
async def on_message(message):
    # Prevent the bot from responding to itself
    if message.author == bot.user:
        return

    # Process commands
    await bot.process_commands(message)

nest_asyncio.apply()
bot.run('MTI0MDQyOTk2MTMyMDQ2NDQ2Nw.Gnb6jm.oQti5bf57n_bLfeCxdtI2DiWJAK0tfSNaHMtHc')