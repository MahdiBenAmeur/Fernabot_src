from sklearn.model_selection import KFold
from rasa.shared.nlu.training_data.loading import load_data
from rasa.model_training import train_nlu
from rasa.model_testing import test_nlu
from rasa.shared.constants import DEFAULT_RESULTS_PATH
from rasa.shared.nlu.training_data.training_data import TrainingData
import os


def train_and_evaluate(train_data_path, test_data_path, config_path, output_path):
    # Train the model
    model_path = train_nlu(config=config_path, nlu_data=train_data_path, output=output_path)

    # Evaluate the model
    evaluation_results = test_nlu(model=model_path, nlu_data=test_data_path, output=output_path)
    return evaluation_results['intent_evaluation']['f1_score']


# Load your data
data_path = '../data/nlu.yml'
training_data = load_data(data_path)

# Setup KFold
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Early stopping parameters
best_score = 0
patience = 2
trigger_times = 0

# Specify paths
config_path = 'config.yml'
output_dir = '../models/'

for fold, (train_index, test_index) in enumerate(kf.split(training_data.training_examples)):
    print(f"Training on fold {fold + 1}/{kf.get_n_splits()}...")

    # Generate train and test data
    train_examples = [training_data.training_examples[i] for i in train_index]
    test_examples = [training_data.training_examples[i] for i in test_index]

    train_data = TrainingData(training_examples=train_examples)
    test_data = TrainingData(training_examples=test_examples)

    # Save training and testing data to disk
    train_data.persist_nlu(os.path.join(output_dir, f"train_data_fold_{fold}.yml"))
    test_data.persist_nlu(os.path.join(output_dir, f"test_data_fold_{fold}.yml"))

    # Train and evaluate the model
    current_score = train_and_evaluate(
        train_data_path=os.path.join(output_dir, f"train_data_fold_{fold}.yml"),
        test_data_path=os.path.join(output_dir, f"test_data_fold_{fold}.yml"),
        config_path=config_path,
        output_path=output_dir
    )

    print(f"Fold {fold + 1} F1 Score: {current_score}")

    # Early stopping logic
    if current_score > best_score:
        best_score = current_score
        trigger_times = 0
    else:
        trigger_times += 1

    if trigger_times >= patience:
        print("Early stopping!")
        break

print("Training completed.")
