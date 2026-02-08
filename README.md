# Othello Game AI Agent

An intelligent game-playing agent for the board game Othello (Reversi) using adversarial search and heuristic evaluation.

This project focuses on designing a decision-making agent capable of competing against baseline strategies by modeling the game as a two-player zero-sum problem and applying classical AI techniques such as minimax search with alpha–beta pruning.

---

## Project Overview

The goal of this project was to implement a competitive Othello agent that can:

- Reason strategically over future board states
- Balance short-term gains against long-term positional advantage
- Evaluate board configurations using handcrafted heuristics
- Compete against provided baseline agents and test harnesses

The agent is implemented in `agent.py`.  
The game engine, GUI, test scripts, and baseline opponents are contained in the `environment/` directory.

---

## Problem Setting

Othello (also known as Reversi) is a deterministic, two-player, turn-based board game played on an 8×8 grid. Players alternate placing discs on the board, capturing opponent pieces by bracketing them in straight lines. The objective is to control the majority of squares by the end of the game.

In this project, the game is modeled as a classical adversarial search problem. At each turn, the agent must select a move under time and depth constraints while anticipating an optimal opponent. Performance is measured by win rate against baseline strategies and by the quality of board positions produced over simulated matches.

---

## Repository Structure

- `agent.py` – My Othello AI agent implementation
- `environment/` – Game engine, GUI, baseline agents, and evaluation utilities

---

## Methods Used

- Minimax search
- Alpha–beta pruning
- Heuristic board evaluation
- Adversarial game modeling
- Depth-limited lookahead
