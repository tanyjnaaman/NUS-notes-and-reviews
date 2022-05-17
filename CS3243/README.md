# CS3243 21/22 S2

## Lecturer
Darren Ler

## Overview of content 
In short, I'd say this is closer to an algorithms course than anything. You learn an interesting amount about how to formulate certain types of problems into "known" problem types, and solve them as an agent (i.e. some artificially "intelligent" construct). Chapters include:
* Informed and uninformed search (problems as search problems)
* Local search (problems where the steps to get there doesn't matter/hard to get)
* Constrain Satisfaction Problems 
* Adverserial Search (Minimax, pruning)
* Logical agents (Logical inference using resolution)
* Uncertainty (Naive Bayes inference and Bayesian networks)

## Grading and exams
The grading consists of 3 2-week long projects (search, local search + CSPs, adverserial search), weekly quizzes, participation, midterm and a final. Was pretty intense. 

## Workload
Honestly, I think this was one of my heavier modules this semester. The content isn't excruciatingly difficult, but the weekly quizzes are pretty annoying (particularly because the style of questions focus on _technical_ correctness - sometimes absolutely asinine edge cases are brought up as counter examples), so be careful when you do them. It got better as the semester progressed as I got used to being careful and spending time on them. 

Secondly, the projects aren't trivial - they do take about 1-2 days on average to complete (about 1 day to finish, 1 hour+ to finalize), but I wouldn't say they're easy. Optimizations through dynamic programming/considerations of time complexity are important because of time limit requirements. 

The midterms and finals were also pretty challenging - in this iteration, particularly, there was a lot of hoo-hah about how tediously difficult the finals were. So get good at computing results quickly. 

## How I studied for it
Dr. Ler seems to have a thing for proofs, so go through the given proofs in tutorials, and for all "given" details (e.g. time complexity), try to prove it to yourself why, and verify it with a TA or something, because one of them will probably come up. (In the midterms, we were asked to prove the time complexity for uniform cost search, and in the final, for alpha-beta pruning with optimal order). 

Secondly, don't start on projects late! They are non-trivial, and will take time, especially to debug. 

Thirdly, particularly for the latter half of the module, get good at tracing the algorithms taught in class (search, AC3, etc.) and get good at computing conditional probabilities. Speed is of the essence, as is correctness. Note that some of the implementations are specific to this module (e.g. in CS2040S, we learn the recursive version of DFS, in here, we use a stack - so the order of exploration differs).

## My thoughts
An interesting introduction to AI solutions. I liked that it formalized the idea of AI not as a black box, but as thinking of problems as mathematical formulations and coming up with algorithms to solve them. 

Dr. Ler is a (in my opinion) a pretty average teacher - he's ambiguous fairly often, sometimes frustratingly tedious with his assessments, but he tries and does seem caring.

This is a compulsory module for CS4248 Natural Language Processing, but is also a generally interesting course to take for a better understanding of "AI" as a field.

## Final grade
Fingers crossed for an A- or A.