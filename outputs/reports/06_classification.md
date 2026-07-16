# Order Profitability Classification

Orders: **39,511** | Profitable: **93.4%** (order profit = line profits - £3.50 handling)

Features: sales, quantity, n_lines, avg_discount, main_category

## Logistic Regression

- Accuracy: **0.950**
- F1 score: **0.974**

```
                precision    recall  f1-score   support

Not profitable       0.82      0.30      0.44       649
    Profitable       0.95      1.00      0.97      9229

      accuracy                           0.95      9878
     macro avg       0.89      0.65      0.71      9878
  weighted avg       0.94      0.95      0.94      9878

```

## Decision Tree (max_depth=6)

- Accuracy: **0.981**
- F1 score: **0.990**

```
                precision    recall  f1-score   support

Not profitable       0.90      0.80      0.85       649
    Profitable       0.99      0.99      0.99      9229

      accuracy                           0.98      9878
     macro avg       0.94      0.90      0.92      9878
  weighted avg       0.98      0.98      0.98      9878

```

## Caveat

Profit labels come from the estimated-cost model (Module 1 assumptions), so scores are optimistic: the models partially re-learn the rule that generated the labels. With real cost data the same pipeline applies unchanged.
