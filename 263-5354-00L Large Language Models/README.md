# 263-5354-00L Large Language Models 22/23 S2

## Lecturer

Ryan Cotterel, Mrinmaya Sachan, Florian Tramer, Ce Zhang

## Overview of content

Context: I did this on a semester abroad at ETH Zurich. I also took the first iteration of the class, so the textbook was *literally being written as I took the class*.

You can find the class website [here](https://rycolab.io/classes/llm-s23/). 

The content is delivered over 15 weeks of instruction, 3 hours of lecture per week, and split into a few key themes. 

1. Theory of language modelling

This part of the class is taught by Ryan and spans the first half of the course. It is *tough*, especially for someone like me who has no background in formal language/automata/measure theory, because we use a lot of concepts from those areas. 

The class begins by introducing formalisms of a (tight) language model as a *probability distribution over (finite) strings*, using bits of measure theory. It then moves onto introducing language modelling/representation learning theoretically - things like gradient descent, maximum likelihood estimation, that kind of stuff. This section covered roughly the first quarter of the class.

The next quarter covers finite state language models, pushdown (context-free) language models, RNN language models and transformer-based language models. The content covered is not at all about building or training models, but purely about modelling them mathematically and then reasoning about their representation capacities - what kind of *languages* (e.g. context-free, regular etc.) can they model? How do we parametrize them? How do we design unbiased and efficient estimators of these parameters? And he covers some interesting proofs (e.g. RNN models are Turing complete computational devices). If you have no background in formal language or automata theory, or prior experience in NLP, buckle up, and please learn ahead. I recommend Stanford's [CS224n](https://web.stanford.edu/class/cs224n/) to ease into NLP and language models more generally.

The first half of the course then rounds out with some bits on text generation (e.g. sampling, tokenization) and current research on it. 

2. Training, fine tuning and inference

This part of the class is taught by Mrinmaya and lasts about a quarter of the course. It is, as described, a lot about current research into training, designing and tuning models. It's a lot closer to what you might expect out of a typical NLP course, but he goes pretty quickly. I found it manageable probably because of prior research experience, but many of my friends who were fresh to ML had a rough time. He covers the timeline (and the important concepts) of the research work on: 

* transfer learning 
* parameter-efficient fine tuning
* prompting and zero-/few-shot inference
* multi-modal LLMs 

It's really good stuff!

3. Parallelism and scaling up, Model analysis, Security and misuse

The remaining quarter of the course is covered by Ce, Ryan and Florian. It includes topics like: 

* Algorithms for distributed training and inference
* Reasoning about data's impact on a model
* Creating datasets and its challenges
* How LLMs scale
* Attacks on LLMs (e.g. injection)
* Safety issues in AI - biases, toxicity, hallucinations, etc.

... and a couple smaller topics. 

They are generally interesting topics and the focus of this part of the course appears more about breadth rather than depth, and works sorta as a showcase of "what's out there". 

## Grading and exams

Because I was an exchange student, I did not take the final exam at the same time as others in the cohort. Instead, I took an oral exam (which was a first for me) - this was 50% of my grade. The remaining 50% came from two 25% assignments. 

Assignment 1 was 5 questions involving mostly proving properties about language models and language modelling using concepts covered in the first half of the class. 

Assignment 2 was 5 questions, mostly programming questions involving training some sort of model or working with some implementation to complete some task. They were very interesting, and not-at-all run of the mill. 

Both assignments were apparently intended to take about 60 hours each, and they did take me about that amount of time (probably more) to complete them.

## Workload

This was a super heavy class. Ryan apparently has a reputation for teaching tough classes, and his reputation remains untouched with this class. Maybe it was also me taking time off to travel, or working full-time during the summer while completing the assignments/studying for the final exam, but I found the class really challenging.

Every week, there were about 20-40 pages of readings (often quite theory-heavy, too) and 3 hours of lectures. I found myself spending about 10 hours a week going through the readings, the lectures, and revising to get the concepts in my head. 

I spent probably about 60-65 hours on both assignments - as designed - and nearing the finals, maybe about 10 hours or so a week (on the weekends) revising the concepts.

A very heavy class, and probably the hardest class I've ever taken.

## How I studied for it

Same as I always do. Did the readings and attended lectures consistently. Asked questions. Made notes. 

## My thoughts

One of the best classes I've ever taken. I'm probably biased because I'm deeply interested in the topic, but I loved how theoretical this class was, because it was very refreshing. If you have any ML experience, you'd know that a lot of this field is very "vibes" based - i.e. empirical. Ryan is one of the leading researchers studying language models from a theoretical angle, and it really shows. I felt like my mind and perspective really expanded from this class. 

The only issue I took with it was that the execution of the class was unpolished - it was the first iteration, and it really showed. Notes were often released late, and there were 0 tutorials (and consequently, 0 practice for the final exam). Assignments, while interesting, were also sometimes unpolished in that the questions were a little imprecise/ambiguous at times. 

But overall, I loved this class, and I cannot recommend it highly enough, especially if you have some NLP background.

## Final grade

I'll update it
