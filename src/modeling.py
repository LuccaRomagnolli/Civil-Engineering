from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier


def build_preprocessor(numerical_columns, categorical_columns):
    return ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_columns),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_columns)
        ]
    )


def build_rf_pipeline(preprocessor, seed):
    return Pipeline(steps=[
        ('preprocess', preprocessor),
        ('model', RandomForestClassifier(
            n_estimators=200,
            random_state=seed,
            n_jobs=-1
        ))
    ])


def build_gbc_pipeline(preprocessor, seed):
    return Pipeline(steps=[
        ('preprocess', preprocessor),
        ('model', GradientBoostingClassifier(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=3,
            random_state=seed
        ))
    ])
