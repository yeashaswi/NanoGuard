# Book 3: Machine Learning from First Principles

This module provides a rigorous mathematical and conceptual exploration of the Machine Learning algorithms powering NanoGuard: **Random Forest Classifiers** for multi-class pollutant identification and **Gradient Boosted Trees** for quantitative concentration regression.

---

## 1. Decision Trees: The Fundamental Building Block

Both Random Forests and Gradient Boosted Trees build upon individual **Classification and Regression Trees (CART)**.

### 1.1 How a Decision Tree Splits Data
Given a dataset $D$ at a tree node with $N$ samples across $C$ pollutant classes:
1. The algorithm evaluates every available feature $x_j$ (e.g., `s4_au_nano`, `lspr_shift_nm`).
2. For each continuous feature, candidate split thresholds $\tau$ are formed by sorting unique values and testing midpoints:
   $$\tau = \frac{x_{(k)} + x_{(k+1)}}{2}$$
3. The dataset is partitioned into two child subsets:
   $$D_{\text{left}} = \{x \in D \mid x_j \le \tau\}, \quad D_{\text{right}} = \{x \in D \mid x_j > \tau\}$$

### 1.2 Splitting Criteria: Gini Impurity
For classification, the quality of a split is quantified using the **Gini Impurity**:

$$I_G(D) = 1 - \sum_{i=1}^C p_i^2$$

Where $p_i$ is the proportion of samples belonging to pollutant class $i$ in node $D$.
* If a node contains only $\text{Ag-NP}$ ($p_{\text{Ag-NP}} = 1$), $I_G = 1 - 1^2 = 0$ (Pure node).
* The algorithm selects the feature $j^*$ and threshold $\tau^*$ that maximize the **Information Gain**:

$$\Delta I_G = I_G(D) - \left[\frac{|D_{\text{left}}|}{|D|} I_G(D_{\text{left}}) + \frac{|D_{\text{right}}|}{|D|} I_G(D_{\text{right}})\right]$$

---

## 2. Random Forest Architecture: Bagging & Subspace Sampling

A single decision tree tends to overfit (high variance). A **Random Forest** resolves this through **Ensemble Learning**.

```
                Training Dataset (2,400 samples)
                   │              │              │
         Bootstrap │    Bootstrap │    Bootstrap │
         Sample 1  │    Sample 2  │    Sample B  │
                   ▼              ▼              ▼
              ┌─────────┐    ┌─────────┐    ┌─────────┐
              │ Tree 1  │    │ Tree 2  │    │ Tree B  │
              │(subset) │    │(subset) │    │(subset) │
              └────┬────┘    └────┬────┘    └────┬────┘
                   │              │              │
             Vote: │        Vote: │        Vote: │
             "TiO2"│        "TiO2"│        "ZnO" │
                   └──────────────┼──────────────┘
                                  ▼
                        Majority Vote / Proba
                           Result: "TiO2"
```

### 2.1 The Variance Reduction Proof
Suppose we average $B$ individual tree estimators, each with variance $\sigma^2$ and pairwise correlation $\rho$:

$$\text{Var}\left(\frac{1}{B} \sum_{b=1}^B T_b(x)\right) = \rho \sigma^2 + \frac{1 - \rho}{B} \sigma^2$$

* As $B \to \infty$, the second term $\frac{1-\rho}{B}\sigma^2 \to 0$.
* The remaining variance is bounded by $\rho \sigma^2$.
* To make $\text{Var}$ as small as possible, we must **minimize correlation $\rho$ between trees**.

### 2.2 How Random Forests De-Correlate Trees
Random Forest introduces two independent layers of stochastic randomization:
1. **Bootstrap Aggregating (Bagging)**: Each of the $B = 150$ trees is trained on an independently drawn bootstrap sample of size $N$ with replacement.
2. **Random Subspace Sampling**: At *every split node*, the algorithm selects a random subset of $m = \sqrt{p}$ features (for $p = 16$ features, $m = 4$). This prevents one dominant sensor (e.g., `s4_au_nano`) from monopolizing the top split in every single tree.

### 2.3 Class Weight Balancing
Industrial sensor logs often have fewer critical leak events than nominal air events. To prevent bias toward the majority class:

$$w_c = \frac{N_{\text{total}}}{C \cdot N_c}$$

Samples of rare classes receive higher weight in the Gini split calculation.

---

## 3. Gradient Boosted Trees: Quantitative Regression

While Random Forests train trees in parallel, **Gradient Boosting** trains trees **sequentially**, with each new tree correcting the residual errors of the existing ensemble.

```
Input x ──► [ Base Tree 1 ] ──► Residual e1 = y - y_hat_1
                                      │
                                      ▼
                            [ Boosted Tree 2 ] ──► Residual e2
                                                        │
                                                        ▼
                                              [ Boosted Tree M ]
                                                        │
                                                        ▼
                        Final Prediction = F_0 + η Σ (Tree_m)
```

### 3.1 Mathematical Formulation
We wish to find a function $\hat{F}(x)$ that minimizes a differentiable loss function $L(y, F(x))$, typically Mean Squared Error for regression:

$$L(y, F(x)) = \frac{1}{2} (y - F(x))^2$$

1. **Initialize** with a constant base value:
   $$F_0(x) = \arg\min_{\gamma} \sum_{i=1}^N L(y_i, \gamma) = \bar{y}$$
2. **Iterate** for $m = 1$ to $M$:
   * Compute the **pseudo-residuals** (negative gradients):
     $$r_{im} = -\left[\frac{\partial L(y_i, F(x_i))}{\partial F(x_i)}\right]_{F=F_{m-1}} = y_i - F_{m-1}(x_i)$$
   * Fit a shallow regression tree $h_m(x)$ to the pseudo-residuals $r_{im}$.
   * Update the model with shrinkage (learning rate $\eta = 0.08$):
     $$F_m(x) = F_{m-1}(x) + \eta \cdot h_m(x)$$

### 3.2 Regularization via Shrinkage & Subsampling
* **Shrinkage ($\eta$)**: Scales each tree's contribution by $0.08$. This forces the ensemble to take small gradient steps, preventing overfitting.
* **Subsampling (`subsample=0.85`)**: Each tree is trained on an $85\%$ random sample of the data (Stochastic Gradient Boosting).

---

## 4. Evaluation Metrics Explained

### 4.1 Classification Metrics

| Metric | Formula | Practical Meaning in Nanoparticle Sensing |
| :--- | :--- | :--- |
| **Accuracy** | $\frac{TP + TN}{TP + TN + FP + FN}$ | Overall percentage of correctly classified emissions. |
| **Precision** | $\frac{TP}{TP + FP}$ | When the model says "$\text{Ag-NP}$", how often is it truly nano-silver? (Low false alarms). |
| **Recall (Sensitivity)** | $\frac{TP}{TP + FN}$ | Out of all true $\text{Ag-NP}$ emissions, how many did the system catch? (Zero missed leaks). |
| **F1-Score** | $2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$ | Harmonic mean balancing false alarms and missed leaks. |

### 4.2 Regression Metrics

$$\text{MAE} = \frac{1}{N}\sum_{i=1}^N |y_i - \hat{y}_i|$$
Measures average absolute error in $\mu\text{g/m}^3$. In our model: $\text{MAE} \approx 4.91\ \mu\text{g/m}^3$.

$$\text{RMSE} = \sqrt{\frac{1}{N}\sum_{i=1}^N (y_i - \hat{y}_i)^2}$$
Penalizes large outlier estimation mistakes heavily. In our model: $\text{RMSE} \approx 14.60\ \mu\text{g/m}^3$.

$$R^2 = 1 - \frac{\sum_{i=1}^N (y_i - \hat{y}_i)^2}{\sum_{i=1}^N (y_i - \bar{y})^2}$$
The coefficient of determination. An $R^2 = 0.9595$ means the model explains **$96.0\%$ of all continuous variance in concentration**.

---

## 5. Avoiding Data Leakage in Scientific Pipelines
1. **Stratified Split**: We split $80\%$ Train / $20\%$ Test with class stratification so every pollutant class is represented proportionally.
2. **Strict Preprocessing Boundaries**:
   * The `StandardScaler` must be computed **strictly on `X_train`** ($\mu_{\text{train}}, \sigma_{\text{train}}$).
   * `X_test` must be transformed using the saved training parameters:
     $$X_{\text{test, scaled}} = \frac{X_{\text{test}} - \mu_{\text{train}}}{\sigma_{\text{train}}}$$
   * Fitting the scaler on the combined dataset leaks test distribution information into training, producing invalid benchmark claims.
