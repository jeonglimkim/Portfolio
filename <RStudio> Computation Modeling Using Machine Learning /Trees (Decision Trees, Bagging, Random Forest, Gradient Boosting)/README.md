## Trees (Decision Trees, Bagging, Random Forest, Gradient Boosting)

### A Conceptual Problem

1.  (15 points) Of the Gini index, classification error, and cross-entropy in simple classification settings with two classes, which would be best to use when *growing* a decision tree? Which would be best to use when *pruning* a decision tree? Why?

-   In the classification setting, RSS cannot be used as a criterion for making the binary splits. A natural alternative to RSS is the classification error rate. However, classification error rate is not sufficiently sensitive for tree-growing, as error rates are less sensitive to poor performing splits. Thus, Gini index and cross-entropy are two methods are better to use as it tend to grow more accurate trees. The classification error rate is preferable if prediction accuracy of the final pruned tree is the goal.
-   Gini is intended for continuous attributes and Entropy is for attributes that occur in classes -Gini is to minimize misclassification -Entropy is for exploratory analysis -Entropy is a little slower to compute.

## An Applied Problem

For the applied portion, your task is to predict attitudes towards racist college professors using the General Social Survey (GSS) survey data. Each respondent was asked *Should a person who believes that Blacks are genetically inferior be allowed to teach in a college or university?* Given the controversy over Richard J. Herrnstein and Charles Murray's [*The Bell Curve*](https://en.wikipedia.org/wiki/The_Bell_Curve) and the ostracization of Nobel laureate [James Watson](https://en.wikipedia.org/wiki/James_Watson) over his controversial views on race and intelligence, this applied task will provide additional insight in the public debate over this issue.

To address this problem, use the `gss_*.csv` data sets, which contain a selection of features from the 2012 GSS. The outcome of interest is `colrac`, which is a binary feature coded as either `ALLOWED` or `NOT ALLOWED`, where 1 means the racist professor *should* be allowed to teach, and 0 means the racist professor *should not* be allowed to teach. Full documentation can be found [here](https://gssdataexplorer.norc.org/variables/vfilter). I preprocessed the data for you to ease the model-fitting process:

-   Missing values have been imputed
-   Categorical features with low-frequency classes collapsed into an "other" category
-   Nominal features with more than two classes have been converted to dummy features
-   Remaining categorical features have been converted to integer values

Your task is to construct a series of models to accurately predict an individual's attitude towards permitting professors who view Blacks to be racially inferior to teach in a college classroom. The learning objectives are:

-   Implement a battery of tree-based learners
-   Tune hyperparameters
-   Substantively interpret models

2.  (35 points) Fit the following four tree-based models predicting `colrac` using the training set (`gss_train.csv`) with 10-fold CV. Remember to tune the relevant hyperparameters for each model as necessary. Only use the tuned model with the best performance for the remaining exercises. **Be sure to leave sufficient *time* for hyperparameter tuning, as grid searches can be quite computationally taxing and take a while.**

    -   Decision tree (the rpart algorithm)
    -   Bagging
    -   Random forest
    -   Gradient boosting

```{r, results = 'hide'}
gss_train <- read_csv("gss_train.csv") 
```

```{r}
gss_train <- gss_train %>% 
  mutate(colrac = as.factor(colrac))

folds <- vfold_cv(data = gss_train, v = 10)

rec <- recipe(colrac ~., data = gss_train)
```

# Decision Tree

```{r, cache = TRUE}
#Decision Tree
set.seed(1234)

dt_mod <- decision_tree(
  cost_complexity = tune(),
  tree_depth = tune(),
  min_n = tune()
  ) %>%
  set_engine("rpart") %>% 
  set_mode("classification")

dt_wf <- workflow() %>%
  add_recipe(rec) %>%
  add_model(dt_mod)

dt_tune_res <- tune_grid(
  dt_wf,
  resamples = folds,
  grid = 30
)
```

# Bagging

```{r, cache = TRUE}
#Bagging
set.seed(1234)

bg_mod <- bag_tree(
  cost_complexity = tune(),
  tree_depth = tune(),
  min_n = tune(),
  ) %>%
  set_engine("rpart", times = 25) %>%
  set_mode("classification")

bg_wf <- workflow() %>%
  add_recipe(rec) %>%
  add_model(bg_mod)

bg_tune_res <- tune_grid(
  bg_wf,
  resamples = folds,
  grid = 30
)
```

# Random Forest

```{r, cache = TRUE}
#Random Forest
set.seed(1234)
rf_mod <- rand_forest(
  mtry = tune(),
  trees = 1000,
  min_n = tune()
) %>%
  set_mode("classification") %>%
  set_engine("ranger")

rf_wf <- workflow() %>%
  add_recipe(rec) %>%
  add_model(rf_mod)

rf_tune_res <- tune_grid(
  rf_wf,
  resamples = folds,
  grid = 30
)
```

# Gradient Boosting

```{r, cache = TRUE}
#Gradient Boosting
set.seed(1234)
xgb_spec <- boost_tree(
  trees = 500, 
  tree_depth = tune(), 
  min_n = tune(), 
  loss_reduction = tune(), 
  sample_size = tune(),
  mtry = tune(), 
  learn_rate = tune(), 
  ) %>% 
  set_mode("classification") %>% 
  set_engine("xgboost") 

xgb_workflow <- workflow() %>% 
  add_recipe(rec) %>% 
  add_model(xgb_spec) 

xgb_grid <- grid_latin_hypercube(
  tree_depth(),
  min_n(),
  loss_reduction(),
  sample_size = sample_prop(),
  finalize(mtry(), gss_train),
  learn_rate(),
  size = 30
)

xgb_tune <-
  tune_grid(
    xgb_workflow, 
    resamples = folds,
    grid = xgb_grid,
    control = control_grid(save_pred = TRUE)
    )
```

# Cross Validated Error Rate, ROC/AUC

3.  (20 points) Compare and present each model's (training) performance based on:

    -   Cross-validated error rate
    -   ROC/AUC

```{r}

dt_tune_res %>% 
  show_best(metric = 'accuracy')

bg_tune_res %>% 
  show_best(metric = 'accuracy')

rf_tune_res %>% 
  show_best(metric = 'accuracy')

xgb_tune %>% 
  show_best(metric = 'accuracy')

```

```{r}

dt_tune_res %>% 
  show_best(metric = 'roc_auc')

bg_tune_res %>% 
  show_best(metric = 'roc_auc')

rf_tune_res %>% 
  show_best(metric = 'roc_auc')

xgb_tune %>% 
  show_best(metric = 'roc_auc')

```

4.  (15 points) Which is the best model? Defend your choice.

-   Although random forest model had a very close accuracy level to the gradient boostingmodel, the gradient boosting model is the best model out of four models. If one carefully tune parameters, gradient boosting can result in better performance than random forest.

5.  (15 points) Evaluate the performance of the best model selected in the previous question using the test set (`gss_test.csv`) by calculating and presenting the classification error rate and AUC of this model. Compared to the fit evaluated on the training set, does this "best" model generalize well? Why or why not? How do you know?

-   Compared to the fit evaluated on the training set, the 'best' model did generalize well. We can see this by calculating the classification error rate and AUC of the model.

```{r, results = 'hide'}
gss_test <- read_csv( "gss_test.csv")

gss_test <- gss_test %>% 
  mutate(colrac = as.factor(colrac))
```

```{r, cache = TRUE}
set.seed(1234)
xgb_spec1 <- boost_tree(
  trees = 500, 
  tree_depth = tune(), 
  min_n = tune(), 
  loss_reduction = tune(), 
  sample_size = tune(),
  mtry = tune(), 
  learn_rate = tune(), 
  ) %>% 
  set_mode("classification") %>% 
  set_engine("xgboost") 

xgb_workflow1 <- workflow() %>% 
  add_recipe(rec) %>% 
  add_model(xgb_spec) 

xgb_grid1 <- grid_latin_hypercube(
  tree_depth(),
  min_n(),
  loss_reduction(),
  sample_size = sample_prop(),
  finalize(mtry(), gss_test),
  learn_rate(),
  size = 30
)

xgb_tune1 <-
  tune_grid(
    xgb_workflow, 
    resamples = folds,
    grid = xgb_grid,
    control = control_grid(save_pred = TRUE)
    )
```

```{r}
xgb_tune1 %>% 
  show_best(metric = 'roc_auc')

xgb_tune1 %>% 
  show_best(metric = 'accuracy')
```
