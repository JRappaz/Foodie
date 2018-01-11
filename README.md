# Foodies

The aim of this project is to gather, process and analyze a recipes social networks data and interactions in order to produce relevant insight about users behaviour and produce meaningful personalized recommendation for recipes.

## Dataset

The data used for this project is from [AllRecipes.com](http://allrecipes.com/), which is considered the biggest recipes social network in the world.

<img src="img/allrecipes-logo.png"  width="410" height="150" />

AllRecipes being very protective of their data, no dataset is provided, hence all data required for the project has been scraped automatically from the website, using python scripts. The whole scraping process can be found in this [Scraper Notebook](python/Scraper.ipynb). The scraping is done in three steps: 

* First by emulating a user browsing the website page by page (20 recipes by pages), until the end, keeping tracks of the recipes links.
* Each recipes link is then explored and all relevant informations about them is stored (Description, ingredients, cooking steps, popularity, etc..). Plus, for each recipes the entire set of reviews with user, rating and comment is downloaded.
* Once all recipes and reviews are downloaded, we create a list of all users that have made at least one comment and we explore all users profiles and download for each of them the list of recipes they have made ("made-it" mention).

The data gathered is then composed of around:

* **60k** Recipes, with their descriptions, ingredients, nutritional facts, preparation steps.
* **3M** Recipe reviews by users, with ratings and text.
* **1M** Users
* **5M** User-Recipes interactions (made-it).

## Data Processing and Analysis

The data analysis aims at providing insight about users behaviour in the social network and recipes popularity trends. The analysis focuses on the implicit interactions of the users with the recipes (The 5M "made-it").

### Users interactions distribution

Figure 1 shows the distribution of interactions amongst users. As expected the distribution follows a power-law. 

<div align="center">
    <img src="img/distribution-user.png" width="800" />
    <p align="center">Figure 1: Users interactions distribution</p>
</div>


It is also interesting to note that 78% of the users have less than 5 interactions.

### Recipes interactions distribution

Figure 2 shows the distribution of interactions amongst recipes. 

We observe that the distribution follows a power-law for the recipes with more than 10 interactions, but is cut for the unpopular recipes. It is highly likely an indicator that AllRecipes deletes unpopular recipes after a certain time.

This intuition is confirmed by the fact that more 30k recipes are present in the users "made-it" but are yet unavailable on the website.

<div align="center">
    <img src="img/distribution-recipe.png" width="800"/>
    <p align="center">Figure 2: Recipe interactions distribution</p>
</div>

## Investigating Recipes Healthiness

As showns by this [study](http://www.christophtrattner.info/pubs/WWW2017.pdf), only a few percentage of the recipes found on AllRecipes are considered healthy according to the World Health Organization.

### Overall Recipes Healthiness

Given all the data obtained from the recipes, it is possible to process them in order to have an idea of how healthy they are according to health standards. The metric used is based on the [Traffic light rating system](https://en.wikipedia.org/wiki/Traffic_light_rating_system) used in some European countries for food labelling. It focuses on 4 main nutritional facts: Fat, Saturated Fat, Sugars and Salt. *cf: Figure 3* 

<div align="center">
    <img src="img/traffic.png" width="570"/>
    <p align="center">Figure 3: Traffic light rating system for food</p>
</div>

It provides a score between 1 (healthy) and 3 (unhealthy) for each 4 facts. The scores of a recipe are additioned in order to produce a unique score between 4 and 12 representing the health score of the recipe. Figure 4 shows the distribution of all recipes of AllRecipes according to their computed health score.

<div align="center">
    <img src="img/health_all.png"/>
    <p align="center">Figure 4: Distribution of recipes health scores</p>
</div>

As expected from the previous study on the AllRecipes health score, relatively few recipes are considered healthy according to the standards.

### Cleaned datasets

After analyizing the dataset and clean the recipes without interactions, it remains in our interacitons dataset around:

* **1M** Users
* **38k** Recipes
* **4.5M** Made-it interactions

### Healthiness by popularity

Figure 5 highlights the health score distribution difference between popular recipes (> 1000 users made it, in transparent blue) and unpopular recipes (< 100 users made it, in traffic light colors).

<div align="center">
    <img src="img/comp_high.png"  />
    <p align="center">Figure 5: Distribution of recipes health scores comparison for high popularity</p>
</div>

This shows that popular recipes tends to be less healthy. 

## Recommender System

*The recommender system models developement is done in this [Model Notebook](./python/Model.ipynb)*

In order to build a recipe recommender system for the users based on their implicit feedback ("made-it"), a [Bayesian Personalized Ranking](https://arxiv.org/abs/1205.2618) (BPR) model is used.

BPR is the optimal model to use for user-personalized items ranking based on implicit feedback, which is exactly what we want to achive in our case.

BPR proceeds by successively selecting positive interactions between a user and a recipe (the user made the recipe) and negative interactions (user didn't make the recipe), and learns with SGD according to wheter or not it ranks the positive and negative interaction properly. The performance of the model is then assessed by computing the AUC score over a test set of the interactions, which represents the expectation that a random positive interaction is ranked before a random negative interaction.

### Popularity Ranker

In order to have a baseline to assess the performance of the recommander model, a dummy popularity ranker is used. This ranker simply ranks recipes by popularities (the number of interactions they have). This is a common unpersonnalized recommender system.

The AUC of the dummy ranker is **83.89%** which is quite high and shows that the popularity of the recipes is highly skewed.

### Simple BPR

The simple BPR model is applied on top of a Matrix Factorization with low-rank matrices P and Q, representing respectively users and recipes. The algorithm successively select random positive and negative interactions and learns with SGD.

With cross-validation of the learning rate alpha, the regularizer lambda and the number of latent factors K we obtain an AUC score of **84.55%**.

### BPR with Bias

It appears that the users interactions with recipes is highly biased by the recipes popularity. Biases are added to the BPR model in order to take this into account.

The model converges faster and we now obtain an AUC score of **84.22%**.

### BPR with non-uniform sampling

### Conclusion on Recommender Systems

The table 1 summarize the performance of the various recommender systems models developed:

| Model             | AUC scores    | Note    										 |
| ------------------|:-------------:|:----------------------------------------------:|
| Popularity Ranker | 83.89% 	    |	 										     |
| Simple BPR        | 84.55%        |	  							    			 |
| BPR with bias     | 84.22%        |										         |
| oversampled BPR (0.75)| 84.22%    |	Performs better on less popularity recipes   |
| oversampled BPR (0.875)| 84.22%   |	Performs better on less popularity recipes   |


## Users Clustering

The table 2 shows the list of 10 most similar recipes for the 10 main clusters of users.

<div align="center">
    <img src="img/clusters_table.png"  />
    <p align="center">Table 2: Most similar recipes for clusters</p>
</div>


