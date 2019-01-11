# Machine Learning for Trading

Implementation of various techniques in machine learning and application in the context of stock trading.

## Contents
- assess_portfolio
	- Computes the daily portfolio value over given date range, and a set of statistics describing performance of the overall portfolio
- assess_learners
	- Implements and evalutes performance of three learning algorithms: Decision Tree, Random Tree, and Bootstrap Aggregation
- defeat_learners
	- A set of simple data-generation functions used to show bias in two ML models.
- manual_strategy
	- Development of a trading strategy using intuition and technical analysis, and testing against a stock using market simulator
- marketsim
	- A market simulator that accepts trading orders and keeps track of a portfolio's value over time and then assesses the performance of that portfolio
- optimize_something
	- Implements a function that can find the optimal allocations for a given set of stocks, optimizing for maximum Sharpe Ratio
- qlearning_robot
	- Implements the Q-Learning and Dyna-Q solutions to the reinforcement learning problem, and applies them to a navigation problem 
- strategy_learner
	- Design of a learning trading agent capable of using technical indicators and a Random Forest learner to learn a profitable trading strategy 

## Dependencies
- ml4-libraries.txt
